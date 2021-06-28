from functools import reduce
from collections import OrderedDict
import json

# used to write and read binary data
import pickle

from block import Block
from transaction import Transaction

from hash_util import hash_block, hash_string_256

MINING_REWARD = 10

blockchain = []
open_transactions = []
participants = {"Maksym"}

owner = "Maksym"


def load_data():
    global blockchain
    global open_transactions

    try:
        with open("blockchain.txt", mode="r") as t:
            file_content = t.readlines()

            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                updated_block = Block(
                    block["index"],
                    block["previous_hash"],
                    [Transaction(tx["sender"], tx["recipient"], tx["amount"]) for tx in block["transactions"]],
                    block["proof"],
                    block["timestamp"],
                )
                updated_blockchain.append(updated_block)

            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []

            for tx in open_transactions:
                updated_transaction = Transaction(tx.sender, tx.recipient, tx.amount)
                updated_transactions.append(updated_transaction)

            open_transactions = updated_transactions
    except (IOError, IndexError):
        GENESIS_BLOCK = Block(0, "", [], 100, 0)

        blockchain = [GENESIS_BLOCK]
        print("File not found")


load_data()


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    tx_sender_open_transactions = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(tx_sender_open_transactions)

    amount_sent = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]

    amount_received = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_recipient, 0)
    print(amount_received - amount_sent)
    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)

    return sender_balance > transaction.amount


def get_last_blockchain_value():
    # add IDE descriptions
    """returns last blockchain value"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)

    return guess_hash[0:2] == "00"


def save_data():
    try:
        with open("blockchain.txt", mode="w") as t:
            saveable_chain = [
                block.__dict__
                for block in [
                    Block(
                        block_el.index,
                        block_el.previous_hash,
                        [tx.__dict__ for tx in block_el.transactions],
                        block_el.proof,
                        block_el.timestamp,
                    )
                    for block_el in blockchain
                ]
            ]

            saveable_tx = [tx.__dict__ for tx in open_transactions]

            t.write(json.dumps(saveable_chain))
            t.write("\n")
            t.write(json.dumps(saveable_tx))
    except IOError:
        print("Save data fail")


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)

    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def add_transaction(recipient, sender=owner, amount=1.0):
    # add IDE descriptions
    """returns last blockchain value

    Arguments:
      :sender: The sender of coins
      :recipient: The recipient of coins
      :amount: The amount of coins

    """

    transaction = Transaction(sender, recipient, amount)

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True

    return False


def mine_block():
    hashed_block = hash_block(blockchain[-1])

    proof = proof_of_work()

    reward_transaction = Transaction("Mining", owner, MINING_REWARD)

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = Block(len(blockchain), hashed_block, copied_transactions, proof)

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
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of work is wrong")
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
            save_data()
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
    elif user_choice == "q":
        break
    else:
        print("Incorrect choice")

    print("Balance of {}: {:6.2f}".format("Maksym", float(get_balance("Maksym"))))
    if not verify_chain():
        print("Not valid blockchain")
        break
