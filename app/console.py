class Console:
    def __init__(self):
        self.init_frame_size = self.get_frame_size()
        self.init_life_number = self.get_life_number()
        self.init_life_cells = self.set_life_cells_positions()

    @staticmethod
    def get_frame_size():
        return [
            int(x) for x in input('Game frame size (rows , columns). Format example: 5, 6 \n').split(",")
        ]

    @staticmethod
    def get_life_number():
        return int(input('Enter number of life cells INTEGER  \n'))

    def set_life_cells_positions(self):
        life_positions = []
        print("Set life cells positions \n __________________")
        for p in range(self.init_life_number):
            print(f"Position # {p + 1}")
            x = int(input("Enter X position: "))
            y = int(input("Enter Y position: "))
            print("\n_________________")
            life_positions.append((x, y))
        return life_positions
