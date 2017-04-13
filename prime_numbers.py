from math import sqrt
numbers_to_find = 1000
numbers_found = 1
prime_numbers_list = [2]
i = 1

while numbers_found < numbers_to_find:
    i += 2
    if (i > 10) and (i % 10 == 5):
        continue
    for j in prime_numbers_list:
        if j > int((sqrt(i)) + 1):
            prime_numbers_list.append(i)
            numbers_found += 1
            break
        if (i % j == 0):
            break
    else:
        prime_numbers_list.append(i)
        numbers_found += 1

print sum(prime_numbers_list)
