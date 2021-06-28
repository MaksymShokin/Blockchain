class Vehicle:
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

    def get_warnings(self):
        print(self.__warnings)
