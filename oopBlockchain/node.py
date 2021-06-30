from uuid import uuid4

from blockchain import Blockchain

from utility.verification import Verification


class Node:
    def __init__(self) -> None:
        # self.id = str(uuid4())
        self.id = "Max"
        self.blockchain = Blockchain(self.id)

    def input_transaction_details(self):
        tx_recipient = input("Please enter recipient name: ")
        tx_amount = float(input("Please enter amount: "))

        return tx_recipient, tx_amount

    def listen_for_input(self):
        while True:
            print("Make a choice: ")
            print("1: Add a new transaction")
            print("2: Mine new block")
            print("3: Output blockchain blocks")
            print("4: Verify transactions")
            print("q: Quit")
            user_choice = input("Your choice: ")

            if user_choice == "1":
                tx_data = self.input_transaction_details()

                recipient, amount = tx_data

                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Transaction succeeded")
                else:
                    print("Transaction failed")

                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                self.blockchain.mine_block()
            elif user_choice == "3":
                for block in self.blockchain.chain:
                    print(block)
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("Some transactions are malformed")
            elif user_choice == "q":
                break
            else:
                print("Incorrect choice")

            print("Balance of {}: {:6.2f}".format(self.id, float(self.blockchain.get_balance())))
            if not Verification.verify_chain(self.blockchain.chain):
                print("Not valid blockchain")
                break


node = Node()
node.listen_for_input()
