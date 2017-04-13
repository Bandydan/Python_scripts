from sys import argv
lines = [line.rstrip('\n').split(';') for line in open(argv[1])]
for line in lines:
    s1, s2 = map(lambda x: set(x.split(',')), line)
    print ','.join(list(s1 & s2).sort())
