from vehicle import Vehicle


class Car(Vehicle):
    def brag():
        print("Nice car!")


car1 = Car()
car1.driving()
car1.add_warning("text")
# car1.__warnings.append('more text')

print(car1)

car2 = Car()
car2.driving()

car3 = Car()
car3.driving()

dict = {"attr": 100, "met": lambda: print("method called")}

print(dict["met"]())
