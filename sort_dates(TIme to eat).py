import sys

test_cases = open(sys.argv[1], 'r')


def process_dates(file_desc):
    for line in file_desc:
        if line[-1] == '\n':
            line = line[:-1]
        list_of_dates = line.split(' ')
        list_of_tuples = []
        for date in list_of_dates:
            date_tuple = tuple(date.split(':'))
            list_of_tuples.append(date_tuple)
        list_of_tuples.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
        list_of_dates = []
        for date_tuple in list_of_tuples:
            list_of_dates.append(':'.join(date_tuple))
        print ' '.join(list_of_dates)

process_dates(test_cases)

test_cases.close()
