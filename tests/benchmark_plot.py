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
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict

class TreeDict(OrderedDict):
    def __missing__(self, key):
        self[key] = value = TreeDict()
        return value

def order_kinds(kinds):
    for idx, kind in enumerate(kinds):
        if kind.startswith('Sorted'):
            del kinds[idx]
            kinds.insert(0, kind)
            break
    return kinds

def test_plot(test):
    ax = plt.gca()
    ax.grid(linestyle='dashed', linewidth=0.5)
    cmap = matplotlib.cm.get_cmap('Set1')
    colors = list(cmap.colors)
    colors[0], colors[1] = colors[1], colors[0]
    del colors[5]
    ax.set_prop_cycle('color', colors)
    kinds = args.kind or list(data[test])
    for order, kind in enumerate(kinds):
        kind_plot(test, kind, len(kinds) - order)
    plt.ylim(ymin=9e-7)
    plt.loglog()
    plt.title(args.name + ' Performance: ' + test)
    plt.ylabel('Seconds')
    plt.xlabel('List Size')
    plt.legend(kinds, loc=2)

def kind_plot(test, kind, zorder):
    sizes = sorted(data[test][kind].keys())
    # Timer isn't any better than micro-second resolution.
    yvalues = [max(1e-6, data[test][kind][size][5]) for size in sizes]
    plt.plot(sizes, yvalues, marker='s', zorder=zorder)

if __name__ == '__main__':
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
    data = TreeDict()
    for line in lines:
        data[line[0]][line[1]][line[2]] = line

    tests = args.test or list(data)

    for test in tests:
        test_plot(test)

        if args.show:
            plt.show()

        if args.save:
            plt.savefig('{0}{1}-{2}.png'.format(args.name, args.suffix, test))

        plt.close()
