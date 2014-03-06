Developing and Contributing
===========================

Collaborators are welcome!

#. Check for open issues or open a fresh issue to start a discussion around a
   bug.  There is a Contributor Friendly tag for issues that should be used by
   people who are not very familiar with the codebase yet.
#. Fork `the repository <https://github.com/grantjenks/sorted_containers>`_ on
   GitHub and start making your changes to a new branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and
   published. :)

Development Lead
----------------

* Grant Jenks <contact@grantjenks.com>

Requests for Contributions
--------------------------

1. Testing / benchmarking with Cython.

2. Testing / benchmarking with PyPy.

3. Better compatibility with blist.

  * Add 'key' option.

4. Better compatibility with rbtree.

  * Pop first item vs. last item.

5. Find a way to allow objects of different types in dict and set types.

6. Add abstract base classes to container types:

  * SortedList: MutableSequence
  * SortedDict: MutableMapping
  * SortedSet: MutableSet
  * KeysView: KeysView, Set, Sequence
  * ValuesView: ValuesView, Sequence
  * ItemsView: ItemsView, Set, Sequence

Development Dependencies
------------------------

Install development dependencies with `pip <http://www.pip-installer.org/>`_:

    > pip install -r requirements.txt

This includes everything for building/running tests, benchmarks and
documentation.

Testing
-------

Testing uses `nose <https://nose.readthedocs.org>`_:

::

    > nosetests --with-coverage
    ...................................................
    Name                          Stmts   Miss  Cover   Missing
    -----------------------------------------------------------
    sortedcontainers                  4      0   100%
    sortedcontainers.sorteddict     220     10    95%   18, 21, 96, 106, 115, 149, 158, 183, 220, 253
    sortedcontainers.sortedlist     452      1    99%   16
    sortedcontainers.sortedset      163     10    94%   51, 62, 65, 70, 75, 80, 84, 86, 88, 90
    -----------------------------------------------------------
    TOTAL                           839     21    97%
    ----------------------------------------------------------------------
    Ran 146 tests in 15.447s
    
    OK

Its normal not to see 100% coverage. Some code is specific to the Python runtime.

There is also stress testing.

::

    > python -m tests.test_stress_sortedlist 1000 0
    Python sys.version_info(major=2, minor=7, micro=0, releaselevel='final', serial=0)
    Setting iterations to 1000
    Setting seed to 0
    Exiting after 0:00:00.846000

If stress exits normally then it worked successfully.

Tested Runtimes
---------------

SortedContainers currently supports the following versions of Python:

* Python 2.6
* Python 2.7
* Python 3.2
* Python 3.3

Life will feel much saner if you use `virtualenv <http://www.virtualenv.org/>`_
to manage each of the runtimes.
