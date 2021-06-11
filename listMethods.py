import functools

simple_list = [1, 2, 3, 4, 5]


def double(num):
    return num * 2


double_list = list(map(double, simple_list))

double_list2 = list(map(lambda el: el * 2, simple_list))


print(double_list)
print(double_list2)

sum_of_numbers = functools.reduce(lambda acc, val: val + acc, simple_list)
print(sum_of_numbers)