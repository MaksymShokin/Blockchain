file = open("demo.txt", mode="w")
file.write("PYTHON")
file.close()


file = open("demo.txt", mode="a")
file.write("is cool")
file.close()


file = open("demo.txt")
file_data = file.read()
print(file_data)
file.close()
