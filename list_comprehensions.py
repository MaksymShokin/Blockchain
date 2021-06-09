simple_list = [1, 2, 3, 4]
doubled_list = [el * 2 for el in simple_list]

print(doubled_list)


simple_list2 = [1, 2, 3, 4]
doubled_list2 = [el * 2 for el in simple_list if el % 2 == 0]


print(doubled_list2)
