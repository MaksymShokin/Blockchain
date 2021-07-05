from collections import OrderedDict


class Transaction:
    def __init__(self, sender, recipient, signature, amount) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([("sender", self.sender), ("recipient", self.recipient), ("signature", self.signature), ("amount", self.amount)])

    def __repr__(self) -> str:
        return str(self.__dict__)
