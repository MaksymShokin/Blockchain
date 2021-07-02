from collections import OrderedDict


class Transaction:
    def __init__(self, sender, recipient, amount) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self):
        return OrderedDict([("sender", self.sender), ("recipient", self.recipient), ("amount", self.amount)])

    def __repr__(self) -> str:
        return str(self.__dict__)