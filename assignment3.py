# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).

# 3) Use a list comprehension to check whether all persons are older than 20.

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).

# 5) Unpack the persons of the original list into different variables and output these variables.

# 1
persons = [
    {"name": "max", "age": 27},
    {"name": "manu", "age": 45},
    {"name": "al", "age": 33},
    {"name": "ss", "age": 25},
]

# 2
person_names = [el["name"] for el in persons]
print(person_names)

# 3

older_then_twenty = all([el["age"] > 20 for el in persons])
print(older_then_twenty)

# 4
import copy

persons_copy = copy.deepcopy(persons)
persons_copy[0]["name"] = "geo"

print(persons)

# 5
a, b, c, d = persons
print(a, b, c, d)
