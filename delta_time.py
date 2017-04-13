from sys import argv
lines = [line.rstrip('\n').split(' ') for line in open(argv[1])]

for time_list in lines:
    t1, t2 = time_list
    if t1 < t2:
        t1, t2 = t2, t1
    t1list = map(int, t1.split(':'))
    t2list = map(int, t2.split(':'))

    if t1list[1] < 0:
        t1list[0] -= 1
        t1list[1] += 60

    delta = []
    for i in xrange(0, 3):
        delta.append(t1list[i] - t2list[i])
        if delta[i] < 0:
            delta[i] += 60
            delta[i-1] -= 1
            if delta[i-1] < 0:
                delta[i-2] -= 1
                delta[i-1] += 60

    for i in xrange(0, 3):
        delta[i] = str(delta[i])
        if len(delta[i]) == 1:
            delta[i] = '0' + delta[i]

    print ':'.join(delta)
