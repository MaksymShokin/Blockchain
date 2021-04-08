blockchain = [[1]]


def get_last_blockchain_value():
    # add IDE descriptions
    """ returns last blockchain value """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(amount, last_transaction=[1]):
   # add IDE descriptions
    """ returns last blockchain value

    Arguments:
      :amount: The amount
      :last_transaction: The last blockchain transaction
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, amount])


def input_amount():
    tx_amount = input('Please enter amount: ')
    add_value(float(tx_amount), get_last_blockchain_value())


# print(blockchain)
while True:
    print('Make a choice: ')
    print('1: Add a new transaction value')
    print('2: Output the new blockchain blocks')
    print('q: Quit')
    user_choice = input('Your choice: ')

    if user_choice == '1':
        input_amount()
    elif user_choice == '2':
        for block in blockchain:
            print(block)
    elif user_choice == 'q':
        break
    else:
        print('Incorrect choice')
