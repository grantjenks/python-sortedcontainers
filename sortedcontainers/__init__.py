"""Sorted Containers -- Sorted List, Sorted Dict, Sorted Set

Sorted Containers is an Apache2 licensed containers library, written in
pure-Python, and fast as C-extensions.

Python's standard library is great until you need a sorted collections
type. Many will attest that you can get really far without one, but the moment
you **really need** a sorted list, dict, or set, you're faced with a dozen
different implementations, most using C-extensions without great documentation
and benchmarking.

In Python, we can do better. And we can do it in pure-Python!

::

    >>> from sortedcontainers import SortedList
    >>> sl = SortedList(['e', 'a', 'c', 'd', 'b'])
    >>> sl
    SortedList(['a', 'b', 'c', 'd', 'e'])
    >>> sl *= 1000000
    >>> sl.count('c')
    1000000
    >>> sl[-3:]
    ['e', 'e', 'e']
    >>> from sortedcontainers import SortedDict
    >>> sd = SortedDict({'c': 3, 'a': 1, 'b': 2})
    >>> sd
    SortedDict({'a': 1, 'b': 2, 'c': 3})
    >>> sd.popitem(index=-1)
    ('c', 3)
    >>> from sortedcontainers import SortedSet
    >>> ss = SortedSet('abracadabra')
    >>> ss
    SortedSet(['a', 'b', 'c', 'd', 'r'])
    >>> ss.bisect_left('c')
    2
    >>> sa = SortedArray('i', [5,7,3,6,2,1,4])
    >>> sa
    SortedArray('i', [1, 2, 3, 4, 5, 6, 7])

Sorted Containers takes all of the work out of Python sorted types - making
your deployment and use of Python easy. There's no need to install a C compiler
or pre-build and distribute custom extensions. Performance is a feature and
testing has 100% coverage with unit tests and hours of stress.

:copyright: (c) 2014-2019 by Grant Jenks.
:license: Apache 2.0, see LICENSE for more details.

"""


from .sortedlist import SortedList, SortedKeyList, SortedListWithKey
from .sortedset import SortedSet
from .sorteddict import (
    SortedDict,
    SortedKeysView,
    SortedItemsView,
    SortedValuesView,
)
from .sortedarray import SortedArray

__all__ = [
    'SortedList',
    'SortedKeyList',
    'SortedListWithKey',
    'SortedDict',
    'SortedKeysView',
    'SortedItemsView',
    'SortedValuesView',
    'SortedSet',
    'SortedArray'
]

__title__ = 'sortedcontainers'
__version__ = '2.4.0'
__build__ = 0x020400
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = '2014-2019, Grant Jenks'
