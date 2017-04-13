import sys
import re

test_cases = open(sys.argv[1], 'r')

regex = '([-0-9]{1,5})'
for line in test_cases:
    regexHandler = re.compile(regex)
    l = map(int, regexHandler.findall(line))
    print int(((l[2] - l[0])**2 + (l[3] - l[1])**2)**0.5)

test_cases.close()
