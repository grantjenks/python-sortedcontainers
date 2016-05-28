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

#. Terabytes of memory for benchmarks of 100,000,000,000 elements.
#. Find a way for SortedSet to inherit directly from ``set``.
#. Testing / benchmarking with Cython.

Get the Code
------------

SortedContainers is actively developed on GitHub, where the code is
`always available <https://github.com/grantjenks/sorted_containers>`_.

You can either clone the public repository::

    $ git clone git://github.com/grantjenks/sorted_containers.git

Download the `tarball <https://github.com/grantjenks/sorted_containers/tarball/master>`_::

    $ curl -OL https://github.com/grantjenks/sorted_containers/tarball/master

Or, download the `zipball <https://github.com/grantjenks/sorted_containers/zipball/master>`_::

    $ curl -OL https://github.com/grantjenks/sorted_containers/zipball/master

Development Dependencies
------------------------

Install development dependencies with `pip <http://www.pip-installer.org/>`_::

    $ pip install -r requirements.txt

This includes everything for building/running tests, benchmarks and
documentation.

Note that installing the Banyan module on Windows requires `patching the source
<https://code.google.com/p/banyan/issues/detail?id=3>`_ in a couple places.

Testing
-------

Testing uses `tox <https://pypi.python.org/pypi/tox>`_. If you don't want to
install all the development requirements, then, after downloading, you can
simply run::

    $ python setup.py test

The test argument to setup.py will download a minimal testing infrastructure
and run the tests.

::

    $ tox
    GLOB sdist-make: /repos/sorted_containers/setup.py
    py26 inst-nodeps: /repos/sorted_containers/.tox/dist/sortedcontainers-0.8.0.zip
    py26 runtests: PYTHONHASHSEED='1205144536'
    py26 runtests: commands[0] | nosetests
    ...
    ----------------------------------------------------------------------
    Ran 150 tests in 7.080s

    OK
    py27 inst-nodeps: /repos/sorted_containers/.tox/dist/sortedcontainers-0.8.0.zip
    py27 runtests: PYTHONHASHSEED='1205144536'
    py27 runtests: commands[0] | nosetests
    ...
    ----------------------------------------------------------------------
    Ran 150 tests in 6.670s

    OK
    py32 inst-nodeps: /repos/sorted_containers/.tox/dist/sortedcontainers-0.8.0.zip
    py32 runtests: PYTHONHASHSEED='1205144536'
    py32 runtests: commands[0] | nosetests
    ...
    ----------------------------------------------------------------------
    Ran 150 tests in 10.254s

    OK
    py33 inst-nodeps: /repos/sorted_containers/.tox/dist/sortedcontainers-0.8.0.zip
    py33 runtests: PYTHONHASHSEED='1205144536'
    py33 runtests: commands[0] | nosetests
    ...
    ----------------------------------------------------------------------
    Ran 150 tests in 10.485s

    OK
    py34 inst-nodeps: /repos/sorted_containers/.tox/dist/sortedcontainers-0.8.0.zip
    py34 runtests: PYTHONHASHSEED='1205144536'
    py34 runtests: commands[0] | nosetests
    ...
    ----------------------------------------------------------------------
    Ran 150 tests in 11.350s

    OK
    ___________________ summary _______________________
      py26: commands succeeded
      py27: commands succeeded
      py32: commands succeeded
      py33: commands succeeded
      py34: commands succeeded
      congratulations :)

Coverage testing uses `nose <https://nose.readthedocs.org>`_:

::

    $ nosetests --with-coverage
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

It's normal not to see 100% coverage. Some code is specific to the Python
runtime.

Stress testing is also based on nose but can be run independently as a
module. Stress tests are kept in the tests directory and prefixed with
test_stress. Stress tests accept two arguments: an iteration count and random
seed value. For example, to run stress on the SortedList data type:

::

    $ python -m tests.test_stress_sortedlist 1000 0
    Python sys.version_info(major=2, minor=7, micro=0, releaselevel='final', serial=0)
    Setting iterations to 1000
    Setting seed to 0
    Exiting after 0:00:00.846000

If stress exits normally then it worked successfully. Some stress is run by tox
and nose but the iteration count is limited at 1,000. More rigorous testing
requires increasing the iteration count to millions. At that level, it's best
to just let it run overnight. Stress testing will stop at the first failure.

Running Benchmarks
------------------

Running and plotting benchmarks is a two step process. Each is a Python script
in the tests directory. To run the benchmarks for SortedList, plot the results,
and save the resulting graphs, run:

::

    $ python -m tests.benchmark_sortedlist --bare > tests/results_sortedlist.txt
    $ python -m tests.benchmark_plot tests/results_sortedlist.txt SortedList --save

Each script has a handful of useful arguments. Use ``--help`` to display
those. Consult the source for details. The file ``tests/benchmark_plot.py``
contains notes about benchmarking different Python runtimes against each other.

If you simply want to run the benchmarks to observe the performance on your
local machine, then run:

::

    $ curl -OL https://github.com/grantjenks/sorted_containers/zipball/master
    $ unzip master
    $ cd grantjenks-sorted_containers-[GITHASH]/
    $ export PYTHONPATH=`pwd`
    $ python -m tests.benchmark_sortedlist
    $ python -m tests.benchmark_sorteddict
    $ python -m tests.benchmark_sortedset

The benchmarks will warn if some packages are not importable. This limits the
possible comparisons. In all cases, you can install missing packages from PyPI.

Tested Runtimes
---------------

SortedContainers actively tests against the following versions of Python:

* CPython 2.6
* CPython 2.7
* CPython 3.2
* CPython 3.3
* CPython 3.4
* CPython 3.5
* PyPy v5.1
* PyPy3 v2.4

Life will feel much saner if you use `virtualenv <http://www.virtualenv.org/>`_
to manage each of the runtimes.
