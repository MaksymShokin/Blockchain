# global variables
# name  = 'Max'

# def get_name():
#   global name
#   name = input('Name: ')


# print function
# print(2+2)


# keyword vs positional arguments
# add_value(float(tx_amount))
# add_value(last_transaction=get_last_blockchain_value(), amount=5)
# add_value(6, get_last_blockchain_value())

# data = [1, 2]
# data2 = [1, 2]

# data == data2
# true
# data is data2
# false

# 1 in data
# True
# 1 not in data 
# False

# there is for else
# and while else 

# using range function
# 
# def verify_chain():
#     block_index = 0
#     is_valid = True

#     for block in blockchain:
#         if block_index == 0:
#             block_index += 1
#             continue
#         elif block[0] != blockchain[block_index - 1]:
#             is_valid = False
#             break
#         block_index += 1

#     return is_valid


# def verify_chain():
#     is_valid = True

#     for block_index in range(len(blockchain)):
#         if block_index == 0:

#             continue
#         elif blockchain[block_index][0] != blockchain[block_index - 1]:
#             is_valid = False
#             break

#     return is_valid 