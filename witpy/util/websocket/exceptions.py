
class WebSocketException(Exception):
    """
    websocket exception class.
    """
    pass


class WebSocketProtocolException(WebSocketException):
    """
    If the websocket protocol is invalid, this exception will be raised.
    """
    pass


class WebSocketPayloadException(WebSocketException):
    """
    If the websocket payload is invalid, this exception will be raised.
    """
    pass


class WebSocketConnectionClosedException(WebSocketException):
    """
    If remote host closed the connection or some network error happened,
    this exception will be raised.
    """
    pass


class WebSocketTimeoutException(WebSocketException):
    """
    WebSocketTimeoutException will be raised at socket timeout during read/write data.
    """
    pass


class WebSocketProxyException(WebSocketException):
    """
    WebSocketProxyException will be raised when proxy error occurred.
    """
    pass


class WebSocketBadStatusException(WebSocketException):
    """
    WebSocketBadStatusException will be raised when we get bad handshake status code.
    """

    def __init__(self, message, status_code, status_message=None, resp_headers=None):
        msg = message % (status_code, status_message)
        super(WebSocketBadStatusException, self).__init__(msg)
        self.status_code = status_code
        self.resp_headers = resp_headers


class WebSocketAddressException(WebSocketException):
    """
    If the websocket address info cannot be found, this exception will be raised.
    """
    pass
