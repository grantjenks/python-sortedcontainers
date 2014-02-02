from __future__ import print_function
from sys import version_info

import time, random, argparse
from collections import OrderedDict

if version_info[0] == 2:
    range = xrange

def measure(test, func, size):
    start = time.clock()
    test(func, size)
    end = time.clock()
    return (end - start)

def benchmark(test, name, ctor, setup, func_name, limit):
    for size in sizes:
        if not args.no_limit and size > limit:
            continue

        # warmup

        obj = ctor()
        setup(obj, size)
        func = getattr(obj, func_name)
        measure(test, func, size)
        
        # record

        times = []
        for rpt in range(5):
            obj = ctor()
            setup(obj, size)
            func = getattr(obj, func_name)
            times.append(measure(test, func, size))

        print(test.func_name, name, size, min(times), max(times), times[2], sum(times) / len(times))

def register_test(func):
    tests[func.func_name] = func
    return func

tests = OrderedDict()
kinds = OrderedDict()
impls = OrderedDict()
sizes = []
lists = {}

parser = argparse.ArgumentParser(description='Benchmarking')
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--no-limit', default=False, action='store_true')
parser.add_argument('--test', action='append')
parser.add_argument('--kind', action='append')
parser.add_argument('--size', type=int, action='append')
args = parser.parse_args()

def main(name):
    global sizes, lists

    print('Benchmarking:', name)

    print('Seed:', args.seed)
    random.seed(args.seed)

    sizes.extend(args.size or [10, 100, 1000, 10000, 100000])

    print('Sizes:', sizes)

    lists.update((key, list(range(key))) for key in sizes)
    for key in sizes:
        random.shuffle(lists[key])

    test_names = args.test or tests.keys()
    kind_names = args.kind or kinds.keys()

    print('Tests:', test_names)
    print('Kinds:', kind_names)

    print('test_name', 'data_type', 'size', 'min', 'max', 'median', 'mean')

    for test in impls:
        if test not in test_names:
            continue
        for name in impls[test]:
            if name not in kind_names:
                continue
            details = impls[test][name]
            benchmark(tests[test], name, details['ctor'], details['setup'], details['func'], details['limit'])

    print('Benchmark Stop')
