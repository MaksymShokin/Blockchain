age = 27
name = 'Max'


def print_my_data():
    print('Max ' + str(age))


print_my_data()


def print_your_data(name, age):
    print(name, str(age))


print_your_data('Alina', 27)


def get_decades_you_lived(age):
    return age // 10


print(get_decades_you_lived(77))