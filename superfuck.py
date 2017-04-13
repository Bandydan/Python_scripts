#!/usr/bin/python2.7
myString = 'g fmnc wms bgblr rpylqjyrc gr zw fylb.\
	rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyrq\
	ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.'
alpha = 'abcdefghijklmnopqrstuvwxyz'
strangeAlpha = alpha[2:] + alpha[:2]
print strangeAlpha[0]
newString = ''
for letter in myString:
	if(alpha.find(letter) != -1):
		newString += strangeAlpha[alpha.find(letter)]
	else:
		newString += letter
print newString

