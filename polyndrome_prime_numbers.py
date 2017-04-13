from math import sqrt
start_from = 999
numbers_found = 1

list_of_poly = []

number = start_from
difference = 10
while number > 10:
    list_of_poly.append(number)
    if (number - difference)/100 < number/100:
        number -= 1
    number -= difference

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

prime_poly = [val for val in list_of_poly if val in prime_numbers_list]
prime_poly.sort(reverse=True)
print prime_poly[0]
