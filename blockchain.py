from functools import reduce
import hashlib
import json

MINING_REWARD = 10
GENESIS_BLOCK = {"previous_hash": "", "index": 0, "transactions": []}

blockchain = [GENESIS_BLOCK]
open_transactions = []
participants = {"Maksym"}

owner = "Maksym"


def hash_block(block):

    return hashlib.sha256(json.dumps(block).encode()).hexdigest()


def get_balance(participant):
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant] for block in blockchain]
    tx_sender_open_transactions = [tx["amount"] for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(tx_sender_open_transactions)

    amount_sent = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_sender, 0)

    tx_recipient = [
        [tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in blockchain
    ]

    amount_received = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_recipient, 0)
    print(amount_received - amount_sent)
    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])

    return sender_balance > transaction["amount"]


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

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True

    return False


def mine_block():
    hashed_block = hash_block(blockchain[-1])

    print(hashed_block)

    reward_transaction = {"sender": "Mining", "recipient": owner, "amount": MINING_REWARD}

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {"previous_hash": hashed_block, "index": len(blockchain), "transactions": copied_transactions}

    blockchain.append(block)
    return True


def input_transaction_details():
    tx_recipient = input("Please enter recipient name: ")
    tx_amount = float(input("Please enter amount: "))

    # add_transaction(owner, tx_recipient, float(tx_amount))
    return tx_recipient, tx_amount


def verify_chain():
    # enumerate returns tuples with indexes
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        elif block["previous_hash"] != hash_block(blockchain[index - 1]):
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


# print(blockchain)
while True:
    print("Make a choice: ")
    print("1: Add a new transaction")
    print("2: Mine new block")
    print("3: Output blockchain blocks")
    print("4: Output participants")
    print("5: Verify transactions")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = input("Your choice: ")

    if user_choice == "1":
        tx_data = input_transaction_details()

        recipient, amount = tx_data

        if add_transaction(recipient, amount=amount):
            print("Transaction succeeded")
        else:
            print("Transaction failed")

        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
    elif user_choice == "3":
        for block in blockchain:
            print(block)
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("Some transactions are malformed")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{"sender": "Chris", "recipient": "Max", "amount": 100}],
            }
    elif user_choice == "q":
        break
    else:
        print("Incorrect choice")

    print("Balance of {}: {:6.2f}".format("Maksym", float(get_balance("Maksym"))))
    if not verify_chain():
        print("Not valid blockchain")
        break
