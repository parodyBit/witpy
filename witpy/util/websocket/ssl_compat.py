
__all__ = ["HAVE_SSL", "ssl", "SSLError", "SSLWantReadError", "SSLWantWriteError"]

try:
    import ssl
    from ssl import SSLError
    from ssl import SSLWantReadError
    from ssl import SSLWantWriteError

    if hasattr(ssl, 'SSLContext') and hasattr(ssl.SSLContext, 'check_hostname'):
        HAVE_CONTEXT_CHECK_HOSTNAME = True
    else:
        HAVE_CONTEXT_CHECK_HOSTNAME = False
        if hasattr(ssl, "match_hostname"):
            from ssl import match_hostname
        __all__.append("match_hostname")
    __all__.append("HAVE_CONTEXT_CHECK_HOSTNAME")

    HAVE_SSL = True
except ImportError:
    # dummy class of SSLError for ssl none-support environment.
    class SSLError(Exception):
        pass


    class SSLWantReadError(Exception):
        pass


    class SSLWantWriteError(Exception):
        pass


    ssl = lambda: None
    HAVE_SSL = False
