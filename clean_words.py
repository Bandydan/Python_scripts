from sys import argv
import re

lines = [line.rstrip('\n') for line in open(argv[1])]
regex = '([a-zA-Z]*)'
regexHandler = re.compile(regex)

for line in lines:
    words_list = [x for x in regexHandler.findall(line.lower())
                  if x != '']
    print ' '.join(words_list)
