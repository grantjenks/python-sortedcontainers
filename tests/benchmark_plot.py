"""
# Plotting Benchmark Results

## Generating Benchmark Results

python -m tests.benchmark_sortedlist > tests\results_sortedlist.txt
python -m tests.benchmark_sorteddict > tests\results_sorteddict.txt
python -m tests.benchmark_sortedset > tests\results_sortedset.txt

## Usage

    usage: benchmark_plot.py [-h] [--test TEST] [--kind KIND] [--show] [--save]
                             filename
    
    Plotting
    
    positional arguments:
      filename     path to file with benchmark data
    
    optional arguments:
      -h, --help   show this help message and exit
      --test TEST
      --kind KIND
      --show
      --save

## Example

    python -m tests.benchmark_plot tests\results_sorteddict.txt --save
"""

from __future__ import print_function

import argparse
import matplotlib.pyplot as plt
from collections import defaultdict

def tree():
    return defaultdict(tree)

parser = argparse.ArgumentParser(description='Plotting')
parser.add_argument('filename', help='path to file with benchmark data')
parser.add_argument('--test', action='append')
parser.add_argument('--kind', action='append')
parser.add_argument('--show', action='store_true')
parser.add_argument('--save', action='store_true')

args = parser.parse_args()

text = open(args.filename).read()

lines = text.splitlines()
lines = [line.split() for line in lines]
del lines[-1]
name = lines[0][1]
header = lines[5]
del lines[0:6]
for line in lines:
    line[2] = int(line[2])
    line[3:] = map(float, line[3:])
data = tree()
for line in lines:
    data[line[0]][line[1]][line[2]] = line

def order_kinds(kinds):
    for idx, kind in enumerate(kinds):
        if kind.startswith('Sorted'):
            del kinds[idx]
            kinds.insert(0, kind)
            break
    return kinds

def test_plot(test):
    kinds = order_kinds(sorted(args.kind or list(data[test])))
    for kind in kinds:
        kind_plot(test, kind)
    plt.loglog()
    plt.title(name + ' Performance: ' + test)
    plt.ylabel('Seconds')
    plt.xlabel('List Size')
    plt.legend(kinds, loc=2)

def kind_plot(test, kind):
    sizes = sorted(data[test][kind].keys())
    yrange = [[(data[test][kind][size][5] - data[test][kind][size][3]) for size in sizes], [(data[test][kind][size][4] - data[test][kind][size][5]) for size in sizes]]
    plt.errorbar(sizes, [data[test][kind][size][5] for size in sizes], yerr=yrange)

tests = args.test or list(data)

for test in tests:
    test_plot(test)

    if args.show:
        plt.show()

    if args.save:
        plt.savefig('{0}-{1}.png'.format(name, test))

    plt.close()
