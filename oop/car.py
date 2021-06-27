class Car:
  top_speed = 100

  def driving(self):
    print(f"I am driving at maximum speed of {self.top_speed}")


car1 = Car()
car1.driving()

dict = {
  "attr": 100,
  "met": lambda: print("method called")
}

print(dict["met"]())