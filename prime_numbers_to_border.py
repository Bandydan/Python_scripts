from math import sqrt
number_to_reach = 1000
prime_numbers_list = [2]
i = 1

while i < number_to_reach:
    i += 2
    if (i > 10) and (i % 10 == 5):
        continue
    for j in prime_numbers_list:
        if j > int((sqrt(i)) + 1):
            prime_numbers_list.append(i)
            break
        if (i % j == 0):
            break
    else:
        prime_numbers_list.append(i)

print prime_numbers_list
