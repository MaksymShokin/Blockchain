print(2+2)

blockchain = [[1]]


def get_last_blockchain_value():
    # add IDE descriptions
    """ returns last blockchain value """
    return blockchain[-1]


def add_value(amount, last_transaction=[1]):
   # add IDE descriptions
    """ returns last blockchain value

    Arguments:
      :amount: The amount
      :last_transaction: The last blockchain transaction
    """
    blockchain.append([last_transaction, amount])


def input_amount():
    tx_amount = input('Please enter amount: ')
    add_value(float(tx_amount), get_last_blockchain_value())


input_amount()
input_amount()
input_amount()

# add_value(float(tx_amount))
# add_value(last_transaction=get_last_blockchain_value(), amount=5)
# add_value(6, get_last_blockchain_value())

print(blockchain)


# name  = 'Max'

# def get_name():
#   global name
#   name = input('Name: ')
