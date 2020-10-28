from windows.arrange_the_ships_window import ArrangeTheShipsWindow


class ArrangeTheShipsLogic:
    def __init__(self, field_size: (int, int), three_dimensional: bool):
        self.field_size = field_size
        self.three_dimensional = three_dimensional
        self.arrange_the_ships_window = None
        self.create_window()

    def create_window(self):
        self.arrange_the_ships_window \
            = ArrangeTheShipsWindow(self.field_size, self.three_dimensional)
        self.arrange_the_ships_window.setupUi()
        self.arrange_the_ships_window.show()

    @staticmethod
    def calculate_the_number_of_ships_on_the_field(size: int) -> dict:
        number_of_cells_for_ships = size // 5
        multiplicity = number_of_cells_for_ships // 20
        number_of_ships = {
            4: 1 * multiplicity,
            3: 2 * multiplicity,
            2: 3 * multiplicity,
            1: 4 * multiplicity
        }
        return number_of_ships
