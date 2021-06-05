blockchain = [[1]]
open_transactions = []

owner = "Maksym"


def get_last_blockchain_value():
    # add IDE descriptions
    """returns last blockchain value"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    # add IDE descriptions
    """returns last blockchain value

    Arguments:
      :sender: The sender of coins
      :recipient: The recipient of coins
      :amount: The amount of coins

    """
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}

    open_transactions.append(transaction)


def mine_block():
    pass


def input_transaction_details():
    tx_recipient = input("Please enter recipient name: ")
    tx_amount = float(input("Please enter amount: "))

    # add_transaction(owner, tx_recipient, float(tx_amount))
    return tx_recipient, tx_amount


def verify_chain():
    block_index = 0
    is_valid = True

    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] != blockchain[block_index - 1]:
            is_valid = False
            break
        block_index += 1

    return is_valid


# print(blockchain)
while True:
    print("Make a choice: ")
    print("1: Add a new transaction value")
    print("2: Output the new blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = input("Your choice: ")

    if user_choice == "1":
        tx_data = input_transaction_details()

        recipient, amount = tx_data

        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        for block in blockchain:
            print(block)
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q":
        break
    else:
        print("Incorrect choice")

    if not verify_chain():
        print("Not valid blockchain")
        break
