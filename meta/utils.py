import contextlib

try:
    from asgiref.local import Local
except ImportError:
    from threading import local as Local  # noqa: N812
_thread_locals = Local()


@contextlib.contextmanager
def set_request(request):
    """
    Context processor that sets the request on the current instance
    """
    _thread_locals._request = request
    yield


def get_request():
    """
    Retrieve request from current instance
    """
    return getattr(_thread_locals, "_request", None)
