import sys


def ref_permute(char_set):
    if 1 == len(char_set):
        set_copy = char_set.copy()
        return [set_copy.pop()]
    else:
        char_list = []
        for char in char_set:
            set_copy = char_set.copy()
            set_copy.remove(char)
            res_list = ref_permute(set_copy)
            if 1 == len(res_list):
                char_list.append([char] + res_list)
            else:
                for temp_list in res_list:
                    char_list.append([char] + temp_list)
        return char_list

test_cases = open(sys.argv[1], 'r')
for line in test_cases:
    if line[-1] == '\n':
        line = line[:-1]
    result = [''.join(lst) for lst in ref_permute(set(line))]
    result.sort()
    print ','.join(result)
