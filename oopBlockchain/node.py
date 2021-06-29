class Node:
    def __init__(self) -> None:
        self.blockchain = []

    def input_transaction_details(self):
        tx_recipient = input("Please enter recipient name: ")
        tx_amount = float(input("Please enter amount: "))

        return tx_recipient, tx_amount

    def user_input(self):
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
                for block in self.blockchain:
                    print(block)
            elif user_choice == "4":
                if verifier.verify_transactions(open_transactions, get_balance):
                    print("All transactions are valid")
                else:
                    print("Some transactions are malformed")
            elif user_choice == "q":
                break
            else:
                print("Incorrect choice")

            print("Balance of {}: {:6.2f}".format("Maksym", float(get_balance("Maksym"))))
            if not verifier.verify_chain(self.blockchain):
                print("Not valid blockchain")
                break
