import sys

file_input = open(sys.argv[1], 'r')

for line in file_input:
    line = line.rstrip()
    fizz, buzz, top = map(int, line.split(' '))
    result = []
    for element in range(1, top+1):
        if (element % fizz == 0) and (element % buzz == 0):
            result.append('FB')
        elif element % fizz == 0:
            result.append('F')
        elif element % buzz == 0:
            result.append('B')
        else:
            result.append(str(element))

    print(' '.join(result))
file_input.close()
