from sys import argv
lines = [line.rstrip('\n') for line in open(argv[1])]

for line in lines:
    info = sum([x.split(':') for x in line.split(',')], [])
    houses = int(info[7])
    info = [int(info[x]) for x in xrange(1, 6, 2)]
    children = sum(info)
    candies = houses * sum([x*y for x, y in zip(info, [3, 4, 5])])/children
    print candies
