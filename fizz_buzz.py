from sys import argv


def fb(f, b, i):
    out = str(i)
    if not i % f:
        out = "F"
    if not i % b:
        if out == "F":
            out += "B"
        else:
            out = "B"
    return out


def fzbz(input):
    f, b, n = map(int, input.split(' '))
    res = [fb(f, b, i) for i in xrange(1, n + 1)]
    return ' '.join(res)


print '\n'.join([fzbz(l.rstrip('\n')) for l in open(argv[1])])
