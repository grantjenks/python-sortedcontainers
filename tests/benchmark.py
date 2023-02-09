
import argparse
import random
import logging
import time
from collections import OrderedDict


def detail(*values, **kwargs):
    if not args.bare:
        print(*values, **kwargs)

def measure(test, func, size):
    start = time.perf_counter()
    test(func, size)
    end = time.perf_counter()
    return (end - start)

def benchmark(test, name, ctor, setup, func_name, limit):
    if args.load > 0:
        load = args.load
        ctor_original = ctor
        def ctor_load():
            obj = ctor_original()
            obj._reset(load)
            return obj
        ctor = ctor_load

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

        times.sort()
        print(getattr(test, '__name__'), name + args.suffix, size, times[0],
              times[-1], times[2], sum(times) / len(times))

def register_test(func):
    tests[getattr(func, '__name__')] = func
    return func

def limit(test, kind, value):
    if kind in impls[test]:
        impls[test][kind]['limit'] = value

def remove(test, kind):
    if kind in impls[test]:
        del impls[test][kind]

tests = OrderedDict()
kinds = OrderedDict()
impls = OrderedDict()
sizes = []
lists = {}

parser = argparse.ArgumentParser(description='Benchmarking')
parser.add_argument('--seed', type=int, default=0,
                    help='seed value for random')
parser.add_argument('--no-limit', default=False, action='store_true',
                    help='no limit on size')
parser.add_argument('--test', action='append', help='filter tests by name')
parser.add_argument('--kind', action='append', help='filter types by name')
parser.add_argument('--size', type=int, action='append',
                    help='specify sizes to test')
parser.add_argument('--suffix', default='', help='suffix for kind name')
parser.add_argument('--bare', action='store_true', default=False,
                    help='hide header and footer info')
parser.add_argument('--load', type=int, default=0,
                    help='load value for sorted container types')
args = parser.parse_args()

def main(name):
    global sizes, lists

    detail('Benchmarking:', name)

    detail('Seed:', args.seed)
    random.seed(args.seed)

    sizes.extend(args.size or [100, 1000, 10000, 100000, 1000000, 10000000])

    detail('Sizes:', sizes)

    lists.update((key, list(range(key))) for key in sizes)
    for key in sizes:
        random.shuffle(lists[key])

    test_names = args.test or tests.keys()
    kind_names = args.kind or kinds.keys()

    detail('Tests:', list(test_names))
    detail('Kinds:', list(kind_names))

    detail('test_name', 'data_type', 'size', 'min', 'max', 'median', 'mean')

    for test in impls:
        if test not in test_names:
            continue
        for name in impls[test]:
            if name not in kind_names:
                continue
            details = impls[test][name]
            try:
                benchmark(
                    tests[test],
                    name,
                    details['ctor'],
                    details['setup'],
                    details['func'],
                    details['limit'],
                )
            except Exception:
                logging.exception('Benchmark Error')
                logging.error('Test: %s', test)
                logging.error('Name: %s', name)
                for key in sorted(details):
                    logging.error('Details[%r]: %s', key, details[key])

    detail('Benchmark Stop')
