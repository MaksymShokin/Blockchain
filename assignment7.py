# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe() ” method (which prints “name” and “kind” in a sentence).

# 2) Try turning describe()  from an instance method into a class and a static method. Change it back to an instance method thereafter.

# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.

# 4) Overwrite a “dunder” method to be able to print your “Food” class.


# 1


class Food:
    def __init__(self, name, kind) -> None:
        self.name = name
        self.kind = kind

    # 4
    def __repr__(self) -> str:
        return "Superprint= {} is {}".format(self.name, self.kind)

    def describe(self):
        print("{} is {}".format(self.name, self.kind))


pizza = Food("pizza", "cheesy")
pizza.describe()

# 2


class FoodStatic:
    @staticmethod
    def describe(name, kind):
        print("{} is {}".format(name, kind))


FoodStatic.describe("pizza", "cheesy")


class FoodClass:
    @classmethod
    def describe(cls, name, kind):
        print("{} is {}".format(name, kind))


FoodClass.describe("pizza", "cheesy")

# 3


class Fruit(Food):
    def __init__(self, name):
        super().__init__("fruit", name)

    def clean(self):
        print("Fruit is cleaned")


class Meat(Food):
    def __init__(self, name):
        super().__init__("meat", name)

    def cook(self):
        print("Meat is cooking")


banana = Fruit("sweet")
banana.describe()
banana.clean()

veal = Meat("tasty")
veal.describe()
veal.cook()

# 4
print(banana)
print(veal)
