import sys

test_cases = open(sys.argv[1], 'r')


def string_mask(file_desc):
    for line in file_desc:
        if line[-1] == '\n':
            line = line[:-1]
        (word, mask) = line.split(' ')
        new_word = ''
        for i in range(0, len(word)):
            letter = word[i]
            if mask[i] == '1':
                letter = letter.upper()
            new_word += letter
        print new_word

string_mask(test_cases)

test_cases.close()
