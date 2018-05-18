Developing and Contributing
===========================

Collaborators are welcome!

#. Check for open issues or open a fresh issue to start a discussion around a
   bug.
#. Fork the `repository`_ on GitHub and start making your changes to a new
   branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and
   published :)

.. _`repository`: https://github.com/grantjenks/python-sortedcontainers

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

    $ git clone git://github.com/grantjenks/python-sortedcontainers.git

.. _`open source`: https://github.com/grantjenks/python-sortedcontainers

Development Dependencies
------------------------

Install development dependencies with `pip`_::

    $ pip install -r requirements.txt

This includes everything for building/running tests, benchmarks and
documentation.

Some alternative implementations, such as `banyan`, may have issues when
installing on Windows. You can still develop :doc:`Sorted Containers<index>`
without these packages. They will be omitted from benchmarking.

.. _`pip`: https://pypi.org/project/pip/

Testing
-------

Testing uses `tox`_. If you don't want to install all the development
requirements, then, after downloading, you can simply run::

    $ python setup.py test

The test argument to `setup.py` will download a minimal testing infrastructure
and run the tests.

::

    $ python setup.py test
    running test
    running egg_info
    writing sortedcontainers.egg-info/PKG-INFO
    writing dependency_links to sortedcontainers.egg-info/dependency_links.txt
    writing top-level names to sortedcontainers.egg-info/top_level.txt
    reading manifest file 'sortedcontainers.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    writing manifest file 'sortedcontainers.egg-info/SOURCES.txt'
    running build_ext
    GLOB sdist-make: /Users/grantj/repos/python-sortedcontainers/setup.py
    py36 inst-nodeps: /Users/grantj/repos/python-sortedcontainers/.tox/dist/sortedcontainers-1.5.10.zip
    py36 installed: attrs==18.1.0,more-itertools==4.1.0,pluggy==0.6.0,py==1.5.3,pytest==3.5.1,six==1.11.0,sortedcontainers==1.5.10
    py36 runtests: PYTHONHASHSEED='365015869'
    py36 runtests: commands[0] | python -m pytest
    ================================================= test session starts =================================================
    platform darwin -- Python 3.6.5, pytest-3.5.1, py-1.5.3, pluggy-0.6.0
    rootdir: /Users/grantj/repos/python-sortedcontainers, inifile: tox.ini
    collected 357 items

    docs/introduction.rst .                                                                                         [  0%]
    sortedcontainers/__init__.py .                                                                                  [  0%]
    sortedcontainers/sorteddict.py ...........                                                                      [  3%]
    sortedcontainers/sortedlist.py .....................................                                            [ 14%]
    sortedcontainers/sortedset.py .................                                                                 [ 18%]
    tests/benchmark_splits_fill.py .                                                                                [ 19%]
    tests/sortedcollection.py .                                                                                     [ 19%]
    tests/test_coverage_sorteddict.py ...................................................                           [ 33%]
    tests/test_coverage_sortedkeylist_modulo.py ................................................................... [ 52%]
    tests/test_coverage_sortedkeylist_negate.py .......................................................             [ 68%]
    tests/test_coverage_sortedlist.py ..........................................................                    [ 84%]
    tests/test_coverage_sortedset.py ..................................................                             [ 98%]
    tests/test_stress_sorteddict.py ..                                                                              [ 98%]
    tests/test_stress_sortedkeylist.py .                                                                            [ 99%]
    tests/test_stress_sortedlist.py .                                                                               [ 99%]
    tests/test_stress_sortedset.py ..                                                                               [100%]

    ============================================= 357 passed in 10.86 seconds =============================================
    lint inst-nodeps: /Users/grantj/repos/python-sortedcontainers/.tox/dist/sortedcontainers-1.5.10.zip
    lint installed: astroid==1.6.4,isort==4.3.4,lazy-object-proxy==1.3.1,mccabe==0.6.1,pylint==1.9.0,six==1.11.0,sortedcontainers==1.5.10,wrapt==1.10.11
    lint runtests: PYTHONHASHSEED='365015869'
    lint runtests: commands[0] | pylint sortedcontainers
    Using config file /Users/grantj/repos/python-sortedcontainers/.pylintrc

    --------------------------------------------------------------------
    Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

    _______________________________________________________ summary _______________________________________________________
      py36: commands succeeded
      lint: commands succeeded

Coverage testing uses `pytest-cov`_:

::

    $ python -m pytest --cov sortedcontainers --cov-report term-missing --cov-branch
    ================================================= test session starts =================================================
    platform darwin -- Python 3.6.5, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
    rootdir: /Users/grantj/repos/python-sortedcontainers, inifile: tox.ini
    plugins: cov-2.5.1, hypothesis-3.55.3
    collected 357 items

    docs/introduction.rst .                                                                                         [  0%]
    sortedcontainers/__init__.py .                                                                                  [  0%]
    sortedcontainers/sorteddict.py ...........                                                                      [  3%]
    sortedcontainers/sortedlist.py .....................................                                            [ 14%]
    sortedcontainers/sortedset.py .................                                                                 [ 18%]
    tests/benchmark_splits_fill.py .                                                                                [ 19%]
    tests/sortedcollection.py .                                                                                     [ 19%]
    tests/test_coverage_sorteddict.py ...................................................                           [ 33%]
    tests/test_coverage_sortedkeylist_modulo.py ................................................................... [ 52%]
    tests/test_coverage_sortedkeylist_negate.py .......................................................             [ 68%]
    tests/test_coverage_sortedlist.py ..........................................................                    [ 84%]
    tests/test_coverage_sortedset.py ..................................................                             [ 98%]
    tests/test_stress_sorteddict.py ..                                                                              [ 98%]
    tests/test_stress_sortedkeylist.py .                                                                            [ 99%]
    tests/test_stress_sortedlist.py .                                                                               [ 99%]
    tests/test_stress_sortedset.py ..                                                                               [100%]

    ---------- coverage: platform darwin, python 3.6.5-final-0 -----------
    Name                             Stmts   Miss Branch BrPart  Cover   Missing
    ----------------------------------------------------------------------------
    sortedcontainers/__init__.py        10      0      0      0   100%
    sortedcontainers/sorteddict.py     159      0     40      0   100%
    sortedcontainers/sortedlist.py    1001      8    420      3    99%   34-39, 44-45, 33->34, 785->787, 1429->1437
    sortedcontainers/sortedset.py      179      0     26      0   100%
    ----------------------------------------------------------------------------
    TOTAL                             1349      8    486      3    99%

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

    $ curl -OL https://github.com/grantjenks/python-sortedcontainers/zipball/master
    $ unzip master
    $ cd grantjenks-python-sortedcontainers-[GITHASH]/
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

Life will feel much saner if you use `venv`_ or `virtualenv`_ and `tox`_ to
manage and test each of the runtimes.

.. _`tox`: https://pypi.org/project/tox/
.. _`pytest-cov`: https://pypi.org/project/pytest-cov/
.. _`venv`: https://docs.python.org/3/library/venv.html
.. _`virtualenv`: https://pypi.org/project/virtualenv/
