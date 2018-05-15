Developing and Contributing
===========================

Collaborators are welcome!

#. Check for open issues or open a fresh issue to start a discussion around a
   bug.
#. Fork `the repository <https://github.com/grantjenks/sorted_containers>`_ on
   GitHub and start making your changes to a new branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and
   published :)

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

:doc:`Sorted Containers<index>` is actively developed on GitHub, where the code
is `open source`_. The recommended way to get a copy of the source repository
is to clone the repository from GitHub::

    $ git clone git://github.com/grantjenks/sorted_containers.git

.. _`open source`: https://github.com/grantjenks/sorted_containers

Development Dependencies
------------------------

Install development dependencies with `pip <https://pypi.org/project/pip/>`_::

    $ pip install -r requirements.txt

This includes everything for building/running tests, benchmarks and
documentation.

Some alternative implementations, such as `banyan`, may have issues when
installing on Windows. You can still develop :doc:`Sorted Containers<index>`
without these packages. They will be omitted from benchmarking.

Testing
-------

Testing uses `tox <https://pypi.org/project/tox/>`_. If you don't want to
install all the development requirements, then, after downloading, you can
simply run::

    $ python setup.py test

The test argument to `setup.py` will download a minimal testing infrastructure
and run the tests.

::

    $ python setup.py test
    <todo>

Coverage testing uses `pytest-cov <https://pypi.org/project/pytest-cov/>`_:

::

    $ todo

It's normal to see coverage a little less than 100%. Some code is specific to
the Python runtime.

Stress testing is also based on pytest but can be run independently as a
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
and pytest but the iteration count is limited at 1,000. More rigorous testing
requires increasing the iteration count to millions. At that level, it's best
to just let it run overnight. Stress testing will stop at the first failure.

Running Benchmarks
------------------

Running and plotting benchmarks is a two step process. Each is a Python script
in the tests directory. To run the benchmarks for :class:`SortedList`, plot the
results, and save the resulting graphs, run:

::

    $ python -m tests.benchmark_sortedlist --bare > tests/results_sortedlist.txt
    $ python -m tests.benchmark_plot tests/results_sortedlist.txt SortedList --save

Each script has a handful of useful arguments. Use ``--help`` to display
those. Consult the source for details. The file `tests/benchmark_plot.py`
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
possible comparisons. See `requirements.txt` for the package names than can be
installed from PyPI.

Tested Runtimes
---------------

:doc:`Sorted Containers<index>` actively tests against the following versions
of Python:

* CPython 2.7
* CPython 3.2
* CPython 3.3
* CPython 3.4
* CPython 3.5
* CPython 3.6
* PyPy
* PyPy3

Life will feel much saner if you use `virtualenv <http://www.virtualenv.org/>`_
and `tox` to manage and test each of the runtimes.
