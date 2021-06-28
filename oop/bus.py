from vehicle import Vehicle


class Bus(Vehicle):
    def __init__(self, top_speed):
        # calling parent constructor
        super().__init__(top_speed)
        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)


bus1 = Bus(150)
bus1.add_warning("Too heavy")
bus1.add_group(["Max", "Oleg", "Tim"])

print(bus1.passengers)
bus1.get_warnings()
bus1.driving()

