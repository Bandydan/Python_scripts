# from sys import argv
# lines = [line.rstrip('\n') for line in open(argv[1])]

# for line in lines:
#     print ' '.join(s[0].upper() + s[1:] for s in line.split(' '))


from sys import argv

f = open(argv[1])
lines = [line.split() for line in f]
a = [map(lambda s: s[0].upper() + s[1:], line) for line in lines]
[lambda s: print " ".join(s) for c in a]

