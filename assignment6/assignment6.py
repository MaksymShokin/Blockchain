# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.

# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.

# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.

# 4) Adjust the logic to load the file content to work with pickled/ json data.

import json


def output_data():
    with open("user_data.txt", mode="r") as t:
        file_content = t.readlines()

        for line in file_content:
            print(line)


def save_input(input):
    with open("user_data.txt", mode="a") as t:
        t.write(json.dumps(input))
        t.write("\n")


while True:
    print("Make you choice")
    print("1. Input data")
    print("2: Output data")
    print("3: Store list data")
    print("q: Quit")

    user_choice = input("Your choice: ")

    if user_choice == "1":
        user_input = input("Data to save: ")
        save_input(user_input)
    elif user_choice == "2":
        output_data()
    elif user_choice == "q":
        print("Exiting")
        break


import json
import pickle

running = True
user_input_list = []

while running:
    print('Please choose')
    print('1: Add input')
    print('2: Output data')
    print('q: Quit')
    user_input = input('Your Choice: ')
    if user_input == '1':
        data_to_store = input('Your text: ')
        user_input_list.append(data_to_store)
        with open('assignment.p', mode='wb') as f:
            # f.write(json.dumps(user_input_list))
            f.write(pickle.dumps(user_input_list))
    elif user_input == '2':
        with open('assignment.p', mode='rb') as f:
            file_content = pickle.loads(f.read())
            for line in file_content:
                print(line)
    elif user_input == 'q':
        running = False
