from time import time


class Block:
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time() if timestamp is None else timestamp

    def __repr__(self) -> str:
        return "Index: {}, previous_hash: {}, transactions: {}, proof: {}".format(
            self.index, self.previous_hash, self.transactions, self.proof
        )
