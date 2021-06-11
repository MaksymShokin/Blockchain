name = "Max"
age = 28

desc = "I am {0} and I am {1} years old and I am {0}".format(name, age)
des2 = "I am {name} and I am {years} years old and I am {name}".format(name=name, years=age)

des6 = f"I am {name} and I am {age:.2f} years old and I am {name}"

print(des6)

print(desc)
print(des2)

funds = 192.8283837

des3 = "Your funds: {:.1f}".format(funds)

des4 = "Your funds: {:-^10.1f}".format(funds)


print(des3)
print(des4)

# escaping chars
des5 = "I\n\"m Max"

print(des5)
