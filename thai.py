#!/usr/bin/python2.7 -tt

f = open('/Users/bandydan/Documents/thai_html.html')
lines = []
for line in f:
  if line.find('THAI') > 0:
    lines.append(line)
thai_symbols = []
for line in lines:
  print line
  point_to_char = line.find('char">') + 6
  point_to_code = line.find('utf8">') + 6
  point_to_name = line.find('name">') + 6
  char = line[point_to_char: line.find('</td>', point_to_char)]
  code = line[point_to_code: line.find('</td>', point_to_code)]
  name = line[point_to_name : line.find('</td>', point_to_name)]
  thai_symbols.append ([name, char, code])
for symbol in thai_symbols:
  print symbol[1], symbol[2], "named =", symbol[0]
