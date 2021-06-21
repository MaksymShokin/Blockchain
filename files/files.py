file = open("demo.txt", mode="a")
file.write("PYTHON")
file.close()


file = open("demo.txt", mode="a")
file.write("is cool")
file.close()


file = open("demo.txt")
file_data = file.read()
print(file_data)
file.close()


# closes file automatically
with open("demo.txt") as t:
    file_data = file.read()
    print(file_data)


# store multiline
# file.write("PYTHON\n")

# read multiline
# file.readlines()
# returns list of strings

# read single line
# file.readline()
