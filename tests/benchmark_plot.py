"""
# Plotting Benchmark Results

## Usage

    usage: benchmark_plot.py [-h] [--test TEST] [--kind KIND] [--show] [--save]
                             filename name

    Plotting

    positional arguments:
      filename     path to file with benchmark data
      name         type name

    optional arguments:
      -h, --help   show this help message and exit
      --test TEST
      --kind KIND
      --show
      --save

"""

from __future__ import print_function

import argparse
import matplotlib.pyplot as plt
from collections import defaultdict

def tree():
    return defaultdict(tree)

parser = argparse.ArgumentParser(description='Plotting')
parser.add_argument('filename', help='path to file with benchmark data')
parser.add_argument('name', help='type name')
parser.add_argument('--test', action='append', help='filter tests by name')
parser.add_argument('--kind', action='append', help='filter types by name')
parser.add_argument('--suffix', default='', help='suffix for output')
parser.add_argument('--show', action='store_true', help='show results')
parser.add_argument('--save', action='store_true', help='save results')

args = parser.parse_args()

text = open(args.filename).read()

lines = text.splitlines()
lines = [line.split() for line in lines]
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
    ax = plt.gca()
    ax.set_color_cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.8'])
    kinds = order_kinds(sorted(args.kind or list(data[test])))
    for kind in kinds:
        kind_plot(test, kind)
    plt.ylim(ymin=9e-7)
    plt.loglog()
    plt.title(args.name + ' Performance: ' + test)
    plt.ylabel('Seconds')
    plt.xlabel('List Size')
    plt.legend(kinds, loc=2)

def kind_plot(test, kind):
    sizes = sorted(data[test][kind].keys())
    yrange = [[(data[test][kind][size][5] - data[test][kind][size][3])
               for size in sizes],
              [(data[test][kind][size][4] - data[test][kind][size][5])
               for size in sizes]]
    # Timer isn't any better than micro-second resolution.
    yvalues = [max(1e-6, data[test][kind][size][5]) for size in sizes]
    plt.errorbar(sizes, yvalues, yerr=yrange)

tests = args.test or list(data)

for test in tests:
    test_plot(test)

    if args.show:
        plt.show()

    if args.save:
        plt.savefig('{0}{1}-{2}.png'.format(args.name, args.suffix, test))

    plt.close()
