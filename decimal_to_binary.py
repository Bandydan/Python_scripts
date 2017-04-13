import sys

test_cases = open(sys.argv[1], 'r')

for line in test_cases:
    if line[-1] == '\n':
        line = line[:-1]
    print int(bin(int(line))[2:])

test_cases.close()
