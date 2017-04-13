from sys import argv
# from mlpy import lcs_std
import string

lines = [line.rstrip('\n').split(';') for line in open(argv[1])]

for line in lines:
    a, b = list(line[0]), list(line[1])
letter_count = dict(zip(string.ascii_lowercase, [0]*26))
print letter_count
