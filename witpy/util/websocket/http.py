
import errno
import os
import socket
import sys

import os
import socket
import struct

from six.moves.urllib.parse import urlparse

from .exceptions import *
from .logging import *
from .socket import*
from .ssl_compat import *

from base64 import encodebytes as base64encode


__all__ = ["proxy_info", "connect", "read_headers"]

try:
    import socks
    ProxyConnectionError = socks.ProxyConnectionError
    HAS_PYSOCKS = True
except:
    class ProxyConnectionError(BaseException):
        pass
    HAS_PYSOCKS = False

class proxy_info(object):

    def __init__(self, **options):
        self.type = options.get("proxy_type") or "http"
        if not(self.type in ['http', 'socks4', 'socks5', 'socks5h']):
            raise ValueError("proxy_type must be 'http', 'socks4', 'socks5' or 'socks5h'")
        self.host = options.get("http_proxy_host", None)
        if self.host:
            self.port = options.get("http_proxy_port", 0)
            self.auth = options.get("http_proxy_auth", None)
            self.no_proxy = options.get("http_no_proxy", None)
        else:
            self.port = 0
            self.auth = None
            self.no_proxy = None




def parse_url(url):
    """
    parse url and the result is tuple of
    (hostname, port, resource path and the flag of secure mode)

    url: url string.
    """
    if ":" not in url:
        raise ValueError("url is invalid")

    scheme, url = url.split(":", 1)

    parsed = urlparse(url, scheme="ws")
    if parsed.hostname:
        hostname = parsed.hostname
    else:
        raise ValueError("hostname is invalid")
    port = 0
    if parsed.port:
        port = parsed.port

    is_secure = False
    if scheme == "ws":
        if not port:
            port = 80
    elif scheme == "wss":
        is_secure = True
        if not port:
            port = 443
    else:
        raise ValueError("scheme %s is invalid" % scheme)

    if parsed.path:
        resource = parsed.path
    else:
        resource = "/"

    if parsed.query:
        resource += "?" + parsed.query

    return hostname, port, resource, is_secure


DEFAULT_NO_PROXY_HOST = ["localhost", "127.0.0.1"]


def _is_ip_address(addr):
    try:
        socket.inet_aton(addr)
    except socket.error:
        return False
    else:
        return True


def _is_subnet_address(hostname):
    try:
        addr, netmask = hostname.split("/")
        return _is_ip_address(addr) and 0 <= int(netmask) < 32
    except ValueError:
        return False


def _is_address_in_network(ip, net):
    ipaddr = struct.unpack('I', socket.inet_aton(ip))[0]
    netaddr, bits = net.split('/')
    netmask = struct.unpack('I', socket.inet_aton(netaddr))[0] & ((2 << int(bits) - 1) - 1)
    return ipaddr & netmask == netmask


def _is_no_proxy_host(hostname, no_proxy):
    if not no_proxy:
        v = os.environ.get("no_proxy", "").replace(" ", "")
        if v:
            no_proxy = v.split(",")
    if not no_proxy:
        no_proxy = DEFAULT_NO_PROXY_HOST

    if hostname in no_proxy:
        return True
    elif _is_ip_address(hostname):
        return any([_is_address_in_network(hostname, subnet) for subnet in no_proxy if _is_subnet_address(subnet)])

    return False


def get_proxy_info(
        hostname, is_secure, proxy_host=None, proxy_port=0, proxy_auth=None,
        no_proxy=None, proxy_type='http'):
    """
    try to retrieve proxy host and port from environment
    if not provided in options.
    result is (proxy_host, proxy_port, proxy_auth).
    proxy_auth is tuple of username and password
     of proxy authentication information.

    hostname: websocket server name.

    is_secure:  is the connection secure? (wss)
                looks for "https_proxy" in env
                before falling back to "http_proxy"

    options:    "http_proxy_host" - http proxy host name.
                "http_proxy_port" - http proxy port.
                "http_no_proxy"   - host names, which doesn't use proxy.
                "http_proxy_auth" - http proxy auth information.
                                    tuple of username and password.
                                    default is None
                "proxy_type"      - if set to "socks5" PySocks wrapper
                                    will be used in place of a http proxy.
                                    default is "http"
    """
    if _is_no_proxy_host(hostname, no_proxy):
        return None, 0, None

    if proxy_host:
        port = proxy_port
        auth = proxy_auth
        return proxy_host, port, auth

    env_keys = ["http_proxy"]
    if is_secure:
        env_keys.insert(0, "https_proxy")

    for key in env_keys:
        value = os.environ.get(key, None)
        if value:
            proxy = urlparse(value)
            auth = (proxy.username, proxy.password) if proxy.username else None
            return proxy.hostname, proxy.port, auth

    return None, 0, None


def _open_proxied_socket(url, options, proxy):
    hostname, port, resource, is_secure = parse_url(url)

    if not HAS_PYSOCKS:
        raise WebSocketException("PySocks module not found.")

    ptype = socks.SOCKS5
    rdns = False
    if proxy.type == "socks4":
        ptype = socks.SOCKS4
    if proxy.type == "http":
        ptype = socks.HTTP
    if proxy.type[-1] == "h":
        rdns = True

    sock = socks.create_connection(
            (hostname, port),
            proxy_type = ptype,
            proxy_addr = proxy.host,
            proxy_port = proxy.port,
            proxy_rdns = rdns,
            proxy_username = proxy.auth[0] if proxy.auth else None,
            proxy_password = proxy.auth[1] if proxy.auth else None,
            timeout = options.timeout,
            socket_options = DEFAULT_SOCKET_OPTION + options.sockopt
    )

    if is_secure:
        if HAVE_SSL:
            sock = _ssl_socket(sock, options.sslopt, hostname)
        else:
            raise WebSocketException("SSL not available.")

    return sock, (hostname, port, resource)


def connect(url, options, proxy, socket):
    if proxy.host and not socket and not (proxy.type == 'http'):
        return _open_proxied_socket(url, options, proxy)

    hostname, port, resource, is_secure = parse_url(url)

    if socket:
        return socket, (hostname, port, resource)

    addrinfo_list, need_tunnel, auth = _get_addrinfo_list(
        hostname, port, is_secure, proxy)
    if not addrinfo_list:
        raise WebSocketException(
            "Host not found.: " + hostname + ":" + str(port))

    sock = None
    try:
        sock = _open_socket(addrinfo_list, options.sockopt, options.timeout)
        if need_tunnel:
            sock = _tunnel(sock, hostname, port, auth)

        if is_secure:
            if HAVE_SSL:
                sock = _ssl_socket(sock, options.sslopt, hostname)
            else:
                raise WebSocketException("SSL not available.")

        return sock, (hostname, port, resource)
    except:
        if sock:
            sock.close()
        raise


def _get_addrinfo_list(hostname, port, is_secure, proxy):
    phost, pport, pauth = get_proxy_info(
        hostname, is_secure, proxy.host, proxy.port, proxy.auth, proxy.no_proxy)
    try:
        # when running on windows 10, getaddrinfo without socktype returns a socktype 0.
        # This generates an error exception: `_on_error: exception Socket type must be stream or datagram, not 0`
        # or `OSError: [Errno 22] Invalid argument` when creating socket. Force the socket type to SOCK_STREAM.
        if not phost:
            addrinfo_list = socket.getaddrinfo(
                hostname, port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
            return addrinfo_list, False, None
        else:
            pport = pport and pport or 80
            # when running on windows 10, the getaddrinfo used above
            # returns a socktype 0. This generates an error exception:
            # _on_error: exception Socket type must be stream or datagram, not 0
            # Force the socket type to SOCK_STREAM
            addrinfo_list = socket.getaddrinfo(phost, pport, 0, socket.SOCK_STREAM, socket.SOL_TCP)
            return addrinfo_list, True, pauth
    except socket.gaierror as e:
        raise WebSocketAddressException(e)


def _open_socket(addrinfo_list, sockopt, timeout):
    err = None
    for addrinfo in addrinfo_list:
        family, socktype, proto = addrinfo[:3]
        sock = socket.socket(family, socktype, proto)
        sock.settimeout(timeout)
        for opts in DEFAULT_SOCKET_OPTION:
            sock.setsockopt(*opts)
        for opts in sockopt:
            sock.setsockopt(*opts)

        address = addrinfo[4]
        err = None
        while not err:
            try:
                sock.connect(address)
            except ProxyConnectionError as error:
                err = WebSocketProxyException(str(error))
                err.remote_ip = str(address[0])
                continue
            except socket.error as error:
                error.remote_ip = str(address[0])
                try:
                    eConnRefused = (errno.ECONNREFUSED, errno.WSAECONNREFUSED)
                except:
                    eConnRefused = (errno.ECONNREFUSED, )
                if error.errno == errno.EINTR:
                    continue
                elif error.errno in eConnRefused:
                    err = error
                    continue
                else:
                    raise error
            else:
                break
        else:
            continue
        break
    else:
        if err:
            raise err

    return sock



def _wrap_sni_socket(sock, sslopt, hostname, check_hostname):
    context = ssl.SSLContext(sslopt.get('ssl_version', ssl.PROTOCOL_SSLv23))

    if sslopt.get('cert_reqs', ssl.CERT_NONE) != ssl.CERT_NONE:
        cafile = sslopt.get('ca_certs', None)
        capath = sslopt.get('ca_cert_path', None)
        if cafile or capath:
            context.load_verify_locations(cafile=cafile, capath=capath)
        elif hasattr(context, 'load_default_certs'):
            context.load_default_certs(ssl.Purpose.SERVER_AUTH)
    if sslopt.get('certfile', None):
        context.load_cert_chain(
            sslopt['certfile'],
            sslopt.get('keyfile', None),
            sslopt.get('password', None),
        )
    context.verify_mode = sslopt['cert_reqs']
    if HAVE_CONTEXT_CHECK_HOSTNAME:
        context.check_hostname = check_hostname
    if 'ciphers' in sslopt:
        context.set_ciphers(sslopt['ciphers'])
    if 'cert_chain' in sslopt:
        certfile, keyfile, password = sslopt['cert_chain']
        context.load_cert_chain(certfile, keyfile, password)
    if 'ecdh_curve' in sslopt:
        context.set_ecdh_curve(sslopt['ecdh_curve'])

    return context.wrap_socket(
        sock,
        do_handshake_on_connect=sslopt.get('do_handshake_on_connect', True),
        suppress_ragged_eofs=sslopt.get('suppress_ragged_eofs', True),
        server_hostname=hostname,
    )


def _ssl_socket(sock, user_sslopt, hostname):
    sslopt = dict(cert_reqs=ssl.CERT_REQUIRED)
    sslopt.update(user_sslopt)

    certPath = os.environ.get('WEBSOCKET_CLIENT_CA_BUNDLE')
    if certPath and os.path.isfile(certPath) \
            and user_sslopt.get('ca_certs', None) is None \
            and user_sslopt.get('ca_cert', None) is None:
        sslopt['ca_certs'] = certPath
    elif certPath and os.path.isdir(certPath) \
            and user_sslopt.get('ca_cert_path', None) is None:
        sslopt['ca_cert_path'] = certPath

    check_hostname = sslopt["cert_reqs"] != ssl.CERT_NONE and sslopt.pop(
        'check_hostname', True)

    sslopt.pop('check_hostname', True)

    sock = ssl.wrap_socket(sock, **sslopt)

    if not HAVE_CONTEXT_CHECK_HOSTNAME and check_hostname:
        match_hostname(sock.getpeercert(), hostname)

    return sock


def _tunnel(sock, host, port, auth):
    debug("Connecting proxy...")
    connect_header = "CONNECT %s:%d HTTP/1.0\r\n" % (host, port)
    # TODO: support digest auth.
    if auth and auth[0]:
        auth_str = auth[0]
        if auth[1]:
            auth_str += ":" + auth[1]
        encoded_str = base64encode(auth_str.encode()).strip().decode().replace('\n', '')
        connect_header += "Proxy-Authorization: Basic %s\r\n" % encoded_str
    connect_header += "\r\n"
    dump("request header", connect_header)

    send(sock, connect_header)

    try:
        status, resp_headers, status_message = read_headers(sock)
    except Exception as e:
        raise WebSocketProxyException(str(e))

    if status != 200:
        raise WebSocketProxyException(
            "failed CONNECT via proxy status: %r" % status)

    return sock


def read_headers(sock):
    status = None
    status_message = None
    headers = {}
    trace("--- response header ---")

    while True:
        line = recv_line(sock)
        line = line.decode('utf-8').strip()
        if not line:
            break
        trace(line)
        if not status:

            status_info = line.split(" ", 2)
            status = int(status_info[1])
            if len(status_info) > 2:
                status_message = status_info[2]
        else:
            kv = line.split(":", 1)
            if len(kv) == 2:
                key, value = kv
                headers[key.lower()] = value.strip()
            else:
                raise WebSocketException("Invalid header")

    trace("-----------------------")
    return status, headers, status_message
