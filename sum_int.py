from sys import argv
numbers = [int(line.rstrip('\n')) for line in open(argv[1])]
sum = 0
for num in numbers:
    sum += num
print sum

print sum(numbers)
for line in numbers:
    print sum(map(int, list(line)))
