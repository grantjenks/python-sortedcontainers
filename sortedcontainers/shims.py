"""Python 2 to 3 Shims

"""

from functools import wraps
from sys import hexversion

if hexversion < 0x03000000:
    from itertools import imap as map
    from itertools import izip as zip
    reduce = reduce
    try:
        from thread import get_ident
    except ImportError:
        from dummy_thread import get_ident
else:
    map = map
    zip = zip
    from functools import reduce
    try:
        from _thread import get_ident
    except ImportError:
        from _dummy_thread import get_ident


def recursive_repr(fillvalue='...'):
    "Decorator to make a repr function return fillvalue for a recursive call."
    # Copied from reprlib in Python 3
    # https://hg.python.org/cpython/file/3.6/Lib/reprlib.py

    def decorating_function(user_function):
        repr_running = set()

        @wraps(user_function)
        def wrapper(self):
            key = id(self), get_ident()
            if key in repr_running:
                return fillvalue
            repr_running.add(key)
            try:
                result = user_function(self)
            finally:
                repr_running.discard(key)
            return result

        return wrapper

    return decorating_function
