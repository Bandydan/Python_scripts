from sys import argv
lines = [line.rstrip('\n') for line in open(argv[1])]
for l in lines:
    l = list(l)
    for i, el in enumerate(l):
        if el.isupper():
            l[i] = el.lower()
        else:
            l[i] = el.upper()
    print ''.join(l)
