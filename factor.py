#!/usr/bin/python2.7
def factorial(x):
	y = 1
	n = x
	if x > 1:
		while x - y > 0:
			n = n * (x - y)
			y +=1 
		return n
	elif x == 0 or x == 1:
		n = 1
	return n

def factor(x):
	if x == 0 or x == 1:
		return 1
	result = x
	counter = x
	while counter > 1:
		result *= counter - 1
		counter -= 1
	return result



print factor(12)
print factorial(12)


