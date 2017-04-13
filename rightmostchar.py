from sys import argv
line = [line.rstrip('\n').split(',') for line in open(argv[1])]
for symbols in line:
    charline, char = symbols
    pos = 0
    while True:
        index = charline.find(char, pos)
        if index == -1:
            break
        elif index > pos:
            pos = index + 1
    print pos-1
