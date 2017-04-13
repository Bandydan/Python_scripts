from sys import argv
symbols_list = [line.rstrip('\n').split(' ') for line in open(argv[1])]
for symbols in symbols_list:
    index = int(symbols[-1])
    symbols = symbols[:-1]
    if index > len(symbols):
        continue
    print symbols[-1 * index]
