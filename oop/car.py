class Car:
    # top_speed = 100

    def __init__(self, top_speed=100) -> None:
        self.top_speed = top_speed
        self.__warnings = []
        # private variable

    def driving(self):
        print(f"I am driving at maximum speed of {self.top_speed}")

    def __repr__(self) -> str:
        print("Printing")

        return "Top speed: {}, warnings: {}".format(self.top_speed, self.__warnings)

    def add_warning(self, warning: str):
        if len(warning) > 0:
            self.__warnings.append(warning)


car1 = Car()
car1.driving()
car1.add_warning('text')
# car1.__warnings.append('more text')

print(car1)

car2 = Car()
car2.driving()

car3 = Car()
car3.driving()

dict = {"attr": 100, "met": lambda: print("method called")}

print(dict["met"]())
