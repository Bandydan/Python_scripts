from sys import argv
lines = [line.rstrip('\n').split('|') for line in open(argv[1])]

for char, code in lines:
    code = map(int, code.lstrip().split(' '))
    S = ''
    for i in code:
        S += char[i-1]
    print S
