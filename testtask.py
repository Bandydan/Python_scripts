goal = {'CPUs': 5, 'RAM': 60, 'DISK': 10}

data = [
    {'name': 't2.micro', 'CPUs': 1,  'RAM': 1.0,  'DISK': 0},
    {'name': 'm1.small', 'CPUs': 1,  'RAM': 1.0,  'DISK': 1},
    {'name': 't2.small', 'CPUs': 1,  'RAM': 2.0,  'DISK': 0},
    {'name': 'm3.medium', 'CPUs': 1,  'RAM': 3.75,  'DISK': 4},
    {'name': 'c3.large', 'CPUs': 2,  'RAM': 3.75,  'DISK': 32},
    {'name': 't2.medium', 'CPUs': 2,  'RAM': 4.0,  'DISK': 0},
    {'name': 'm3.large', 'CPUs': 2,  'RAM': 7.5,  'DISK': 32},
    {'name': 'r3.large', 'CPUs': 2,  'RAM': 15.0,  'DISK': 32},
    {'name': 'c3.xlarge', 'CPUs': 4,  'RAM': 7.5,  'DISK': 80},
    {'name': 'm3.xlarge', 'CPUs': 4,  'RAM': 15.0,  'DISK': 80},
    {'name': 'r3.xlarge', 'CPUs': 4,  'RAM': 30.5,  'DISK': 80},
    {'name': 'i2.xlarge', 'CPUs': 4,  'RAM': 30.5,  'DISK': 800},
    {'name': 'g2.2xlarge', 'CPUs': 8,  'RAM': 15.0,  'DISK': 60},
    {'name': 'c3.2xlarge', 'CPUs': 8,  'RAM': 15.0,  'DISK': 160},
    {'name': 'm3.2xlarge', 'CPUs': 8,  'RAM': 30.0,  'DISK': 160},
    {'name': 'r3.2xlarge', 'CPUs': 8,  'RAM': 61.0,  'DISK': 160},
    {'name': 'i2.2xlarge', 'CPUs': 8,  'RAM': 61.0,  'DISK': 1600},
    {'name': 'c3.4xlarge', 'CPUs': 16,  'RAM': 30.0,  'DISK': 320},
    {'name': 'hs1.8xlarge', 'CPUs': 16,  'RAM': 117.0,  'DISK': 49152},
    {'name': 'r3.4xlarge', 'CPUs': 16,  'RAM': 122.0,  'DISK': 320},
    {'name': 'i2.4xlarge', 'CPUs': 16,  'RAM': 122.0,  'DISK': 3200},
    {'name': 'c3.8xlarge', 'CPUs': 32,  'RAM': 60.0,  'DISK': 640},
    {'name': 'r3.8xlarge', 'CPUs': 32,  'RAM': 244.0,  'DISK': 640},
    {'name': 'i2.8xlarge', 'CPUs': 32,  'RAM': 244.0,  'DISK': 6400}
]

for element in data:
    if element['CPUs'] >= goal['CPUs'] and element['RAM'] >= goal['RAM'] and element['DISK'] >= goal['DISK']:
        print element['name']
        break




