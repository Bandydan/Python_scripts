from sys import argv
numbers = [int(line.rstrip('\n')) for line in open(argv[1])]

fibs = [1, 1]
for l in xrange(2, max(numbers) + 1):
    fibs.append(fibs[l-1] + fibs[l-2])

for number in numbers:
    if number == 0:
        print 0
    else:
        print fibs[number-1]
