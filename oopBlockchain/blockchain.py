from functools import reduce
import json
import requests
from requests.api import request

# used to write and read binary data

from block import Block
from transaction import Transaction

from utility.verification import Verification
from utility.hash_util import hash_block
from wallet import Wallet


MINING_REWARD = 10

owner = "Maksym"


class Blockchain:
    def __init__(self, hosting_node_id, port) -> None:
        GENESIS_BLOCK = Block(0, "", [], 100, 0)

        self.chain = [GENESIS_BLOCK]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.__peer_of_nodes = set()
        self.port = port
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @property
    def all_nodes(self):
        return list(self.__peer_of_nodes)

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open("blockchain-{}.txt".format(self.port), mode="r") as t:
                file_content = t.readlines()

                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    updated_block = Block(
                        block["index"],
                        block["previous_hash"],
                        [
                            Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"])
                            for tx in block["transactions"]
                        ],
                        block["proof"],
                        block["timestamp"],
                    )
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []

                for tx in open_transactions:
                    updated_transaction = Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"])
                    updated_transactions.append(updated_transaction)

                self.open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_of_nodes = set(peer_nodes)
        except (IOError, IndexError):
            print("File not found")

    def save_data(self):
        try:
            with open("blockchain-{}.txt".format(self.port), mode="w") as t:
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
                        for block_el in self.__chain
                    ]
                ]

                saveable_tx = [tx.__dict__ for tx in self.get_open_transactions()]

                t.write(json.dumps(saveable_chain))
                t.write("\n")
                t.write(json.dumps(saveable_tx))
                t.write("\n")
                t.write(json.dumps(list(self.__peer_of_nodes)))
        except IOError:
            print("Save data fail")

    def add_block(self, block):
        transactions = [
            Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"]) for tx in block["transactions"]
        ]

        proof_is_valid = Verification.valid_proof(transactions[:-1], block["previous_hash"], block["proof"])
        hashes_match = hash_block(self.chain[-1]) == block["previous_hash"]

        if not proof_is_valid or not hashes_match:
            return False

        converted_block = Block(
            block["index"], block["previous_hash"], transactions, block["proof"], block["timestamp"]
        )

        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block["transactions"]:
            for opentx in stored_transactions:
                if (
                    opentx.sender == itx["sender"]
                    and opentx.recipient == itx["recipient"]
                    and opentx.amount == itx["amount"]
                    and opentx.signature == itx["signature"]
                ):
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print("Item was already removed")
        self.save_data()
        return True

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)

        proof = 0

        while not Verification.valid_proof(self.get_open_transactions(), last_hash, proof):
            proof += 1

        return proof

    def get_balance(self, sender=None):
        if sender == None:
            if self.hosting_node == None:
                return None
            participant = self.hosting_node

        else:
            participant = sender

        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        tx_sender_open_transactions = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(tx_sender_open_transactions)

        amount_sent = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_sender, 0)

        tx_recipient = [
            [tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain
        ]

        amount_received = reduce(lambda acc, val: acc + sum(val) if len(val) > 0 else acc + 0, tx_recipient, 0)
        print(amount_received - amount_sent)
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        # add IDE descriptions
        """returns last blockchain value"""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0, is_receiving=False):
        # add IDE descriptions
        """returns last blockchain value

        Arguments:
          :sender: The sender of coins
          :recipient: The recipient of coins
          :signature: The signature of transaction
          :amount: The amount of coins
        """

        # if self.hosting_node == None:
        #     return False

        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            if not is_receiving:
                for node in self.__peer_of_nodes:
                    url = "http://{}/broadcast-transaction".format(node)
                    try:
                        response = requests.post(
                            url,
                            json={"sender": sender, "recipient": recipient, "amount": amount, "signature": signature},
                        )

                        if response.status_code == 400:
                            print("client error")
                        elif response.status_code == 500:
                            print("server error")

                    except request.exception.ConnectionError:
                        continue
            return True

        return False

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_of_nodes:
            url = "http://{}/chain".format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [
                    Block(
                        block["index"],
                        block["previous_hash"],
                        [
                            Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"])
                            for tx in block["transactions"]
                        ],
                        block["proof"],
                        block["timestamp"],
                    )
                    for block in node_chain
                ]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def mine_block(self):
        if self.hosting_node == None:
            return None

        hashed_block = hash_block(self.__chain[-1])

        proof = self.proof_of_work()

        reward_transaction = Transaction("Mining", self.hosting_node, "", MINING_REWARD)

        copied_transactions = self.get_open_transactions()
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        for node in self.__peer_of_nodes:
            url = "http://{}/broadcast-block".format(node)
            converted_block = block.__dict__.copy()
            converted_block["transactions"] = [tx.__dict__ for tx in converted_block["transactions"]]

            try:
                response = requests.post(url, json={"block": converted_block},)

                if response.status_code == 400:
                    print("block client error")
                elif response.status_code == 500:
                    print("block server error")
                elif response.status_code == 409:
                    self.resolve_conflicts = True

            except request.exception.ConnectionError:
                continue
        return block

    def add_peer_node(self, node):
        """Function that adds peer node to the set
          Arguments:
            :node: Node url
        """
        self.__peer_of_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Function that removes peer node from the set
          Arguments:
            :node: Node url
        """
        self.__peer_of_nodes.discard(node)
        self.save_data()
