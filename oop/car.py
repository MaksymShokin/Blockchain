class Car:
    # top_speed = 100

    def __init__(self, top_speed=100) -> None:
        self.top_speed = top_speed
        self.warnings = []

    def driving(self):
        print(f"I am driving at maximum speed of {self.top_speed}")


car1 = Car()
car1.driving()

car2 = Car()
car2.driving()

car3 = Car()
car3.driving()

dict = {"attr": 100, "met": lambda: print("method called")}

print(dict["met"]())
