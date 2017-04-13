from sys import argv
line = [map(int, line.rstrip('\n').split(',')) for line in open(argv[1])]
for elems in line:
    n, m = elems
    while True:
        n -= m
        if n < 0:
            n += m
            print n
            break
