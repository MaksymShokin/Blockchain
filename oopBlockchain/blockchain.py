from functools import reduce
import json

# used to write and read binary data

from block import Block
from transaction import Transaction
from verification import Verification

from hash_util import hash_block


MINING_REWARD = 10

owner = "Maksym"

verifier = Verification()


class Blockchain:
    def __init__(self) -> None:
        GENESIS_BLOCK = Block(0, "", [], 100, 0)

        self.chain = [GENESIS_BLOCK]
        self.open_transactions = []
        self.load_data()

    def load_data(self):
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

                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []

                for tx in open_transactions:
                    updated_transaction = Transaction(tx.sender, tx.recipient, tx.amount)
                    updated_transactions.append(updated_transaction)

                self.open_transactions = updated_transactions
        except (IOError, IndexError):
            print("File not found")

    def save_data(self):
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
                        for block_el in self.chain
                    ]
                ]

                saveable_tx = [tx.__dict__ for tx in self.open_transactions]

                t.write(json.dumps(saveable_chain))
                t.write("\n")
                t.write(json.dumps(saveable_tx))
        except IOError:
            print("Save data fail")

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)

        proof = 0

        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1

        return proof

    def get_balance(self, participant):
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.chain]
        tx_sender_open_transactions = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(tx_sender_open_transactions)

        amount_sent = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.chain]

        amount_received = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_recipient, 0)
        print(amount_received - amount_sent)
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        # add IDE descriptions
        """returns last blockchain value"""
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient, sender=owner, amount=1.0):
        # add IDE descriptions
        """returns last blockchain value

        Arguments:
          :sender: The sender of coins
          :recipient: The recipient of coins
          :amount: The amount of coins

        """

        transaction = Transaction(sender, recipient, amount)

        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True

        return False

    def mine_block(self, node):
        hashed_block = hash_block(self.chain[-1])

        proof = self.proof_of_work()

        reward_transaction = Transaction("Mining", node, MINING_REWARD)

        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        block = Block(len(self.chain), hashed_block, copied_transactions, proof)

        self.chain.append(block)
        return True
