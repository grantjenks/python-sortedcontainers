#!/bin/bash

set -x

# Compare Implementations

echo ". env36/bin/activate && python -m tests.benchmark_sortedlist --bare > tests/results_sortedlist.txt" | bash
python -m tests.benchmark_plot tests/results_sortedlist.txt SortedList --save

echo ". env36/bin/activate && python -m tests.benchmark_sorteddict --bare > tests/results_sorteddict.txt" | bash
python -m tests.benchmark_plot tests/results_sorteddict.txt SortedDict --save

echo ". env36/bin/activate && python -m tests.benchmark_sortedset --bare > tests/results_sortedset.txt" | bash
python -m tests.benchmark_plot tests/results_sortedset.txt SortedSet --save

# Compare Python Versions

rm tests/results_runtime_sortedlist.txt
echo ". env36/bin/activate && python -m tests.benchmark_sortedlist --bare --kind SortedList --suffix _Py36 >> tests/results_runtime_sortedlist.txt" | bash
echo ". env27/bin/activate && python -m tests.benchmark_sortedlist --bare --kind SortedList --suffix _Py27 >> tests/results_runtime_sortedlist.txt" | bash
echo ". env27/bin/activate && pypy -m tests.benchmark_sortedlist --bare --kind SortedList --suffix _PyPy >> tests/results_runtime_sortedlist.txt" | bash
python -m tests.benchmark_plot tests/results_runtime_sortedlist.txt SortedList --suffix _runtime --save

rm tests/results_runtime_sorteddict.txt
echo ". env36/bin/activate && python -m tests.benchmark_sorteddict --bare --kind SortedDict --suffix _Py36 >> tests/results_runtime_sorteddict.txt" | bash
echo ". env27/bin/activate && python -m tests.benchmark_sorteddict --bare --kind SortedDict --suffix _Py27 >> tests/results_runtime_sorteddict.txt" | bash
echo ". env27/bin/activate && pypy -m tests.benchmark_sorteddict --bare --kind SortedDict --suffix _PyPy >> tests/results_runtime_sorteddict.txt" | bash
python -m tests.benchmark_plot tests/results_runtime_sorteddict.txt SortedDict --suffix _runtime --save

rm tests/results_runtime_sortedset.txt
echo ". env36/bin/activate && python -m tests.benchmark_sortedset --bare --kind SortedSet --suffix _Py36 >> tests/results_runtime_sortedset.txt" | bash
echo ". env27/bin/activate && python -m tests.benchmark_sortedset --bare --kind SortedSet --suffix _Py27 >> tests/results_runtime_sortedset.txt" | bash
echo ". env27/bin/activate && pypy -m tests.benchmark_sortedset --bare --kind SortedSet --suffix _PyPy >> tests/results_runtime_sortedset.txt" | bash
python -m tests.benchmark_plot tests/results_runtime_sortedset.txt SortedSet --suffix _runtime --save

# Compare Loads

rm tests/results_load_sortedlist.txt
echo ". env36/bin/activate && python -m tests.benchmark_sortedlist --bare --kind SortedList --suffix _100 --load 100 --no-limit >> tests/results_load_sortedlist.txt" | bash
echo ". env36/bin/activate && python -m tests.benchmark_sortedlist --bare --kind SortedList --suffix _1000 --load 1000 --no-limit >> tests/results_load_sortedlist.txt" | bash
echo ". env36/bin/activate && python -m tests.benchmark_sortedlist --bare --kind SortedList --suffix _10000 --load 10000 --no-limit >> tests/results_load_sortedlist.txt" | bash
python -m tests.benchmark_plot tests/results_load_sortedlist.txt SortedList --suffix _load --save

rm tests/results_load_sorteddict.txt
echo ". env36/bin/activate && python -m tests.benchmark_sorteddict --bare --kind SortedDict --suffix _100 --load 100 --no-limit >> tests/results_load_sorteddict.txt" | bash
echo ". env36/bin/activate && python -m tests.benchmark_sorteddict --bare --kind SortedDict --suffix _1000 --load 1000 --no-limit >> tests/results_load_sorteddict.txt" | bash
echo ". env36/bin/activate && python -m tests.benchmark_sorteddict --bare --kind SortedDict --suffix _10000 --load 10000 --no-limit >> tests/results_load_sorteddict.txt" | bash
python -m tests.benchmark_plot tests/results_load_sorteddict.txt SortedDict --suffix _load --save

rm tests/results_load_sortedset.txt
echo ". env36/bin/activate && python -m tests.benchmark_sortedset --bare --kind SortedSet --suffix _100 --load 100 --no-limit >> tests/results_load_sortedset.txt" | bash
echo ". env36/bin/activate && python -m tests.benchmark_sortedset --bare --kind SortedSet --suffix _1000 --load 1000 --no-limit >> tests/results_load_sortedset.txt" | bash
echo ". env36/bin/activate && python -m tests.benchmark_sortedset --bare --kind SortedSet --suffix _10000 --load 10000 --no-limit >> tests/results_load_sortedset.txt" | bash
python -m tests.benchmark_plot tests/results_load_sortedset.txt SortedSet --suffix _load --save
