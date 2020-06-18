
import logging

_logger = logging.getLogger('websocket')
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

_logger.addHandler(NullHandler())

_traceEnabled = False

__all__ = ["enableTrace", "dump", "error", "warning", "debug", "trace",
           "isEnabledForError", "isEnabledForDebug", "isEnabledForTrace"]


def enableTrace(traceable, handler=logging.StreamHandler()):
    """
    turn on/off the traceability.

    traceable: boolean value. if set True, traceability is enabled.
    """
    global _traceEnabled
    _traceEnabled = traceable
    if traceable:
        _logger.addHandler(handler)
        _logger.setLevel(logging.DEBUG)


def dump(title, message):
    if _traceEnabled:
        _logger.debug("--- " + title + " ---")
        _logger.debug(message)
        _logger.debug("-----------------------")


def error(msg):
    _logger.error(msg)


def warning(msg):
    _logger.warning(msg)


def debug(msg):
    _logger.debug(msg)


def trace(msg):
    if _traceEnabled:
        _logger.debug(msg)


def isEnabledForError():
    return _logger.isEnabledFor(logging.ERROR)


def isEnabledForDebug():
    return _logger.isEnabledFor(logging.DEBUG)


def isEnabledForTrace():
    return _traceEnabled
