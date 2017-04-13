import sys

test_cases = open(sys.argv[1], 'r')

for line in test_cases:
    (num_of_zeros, number) = map(int, line.split(' '))
    counter = 0
    for i in range(1, number+1):
        binary_str = str(bin(i))[2:]
        if (binary_str.count('0')) == num_of_zeros:
            counter += 1
    print counter

test_cases.close()
