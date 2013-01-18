def add_inc(count, load):
    from sortedlist import SortedList
    slst = SortedList(load=load)
    for val in xrange(count):
        slst.add(val)

def add_dec(count, load):
    from sortedlist import SortedList
    slst = SortedList(load=load)
    for val in xrange(count, 0, -1):
        slst.add(val)

def add_rnd(count, load):
    from sortedlist import SortedList
    import random
    random.seed(0)
    slst = SortedList(load=load)
    for val in xrange(count):
        slst.add(random.random())

def fun_rnd(count):
    import random
    random.seed(0)
    for val in xrange(count):
        random.random()

def calibrate(command, setup):
    import timeit
    number = 1
    while True:
        dur = timeit.timeit(command, setup=setup, number=number)
        if dur > 1: break
        number *= 2
    return number

def stddev(values):
    mean = sum(values) / len(values)
    diff = [(value - mean) ** 2 for value in values]
    return (sum(diff) / len(values)) ** 0.5

def better_timeit(command, setup, repeat=5):
    import timeit
    number = calibrate(command, setup)
    print 'Testing "', command, '" at', number, 'iterations.'
    runs = []
    for rpt in xrange(repeat):
        runs.append(timeit.timeit(command, setup=setup, number=number) / number)
    print 'Min:', min(runs), 'Max:', max(runs), 'Mean:', sum(runs) / repeat,
    print 'Median:', sorted(runs)[repeat / 2], 'Stddev:', stddev(runs)

if __name__ == '__main__':
    # At 1,000,000 - load=100
    for val in xrange(50, 151, 50):
        better_timeit('add_rnd(10000000, {})'.format(val), 'from __main__ import add_rnd')
