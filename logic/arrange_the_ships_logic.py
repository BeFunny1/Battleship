import collections
from itertools import repeat

from windows.arrange_the_ships_window import ArrangeTheShipsWindow


class ArrangeTheShipsLogic:
    def __init__(self, field_size: (int, int), three_dimensional: bool):
        self.field_size = field_size
        self.three_dimensional = three_dimensional
        self.arrange_the_ships_window = None
        self.stack_ships = []
        self.field_for_ships = self.create_start_field_for_ships()
        self.create_an_environment()

    def processing_options_for_the_location_of_the_ship(
            self, level: int, point: (int, int)):
        activate_del = self.arrange_the_ships_window.button_del_activity
        if not self.is_a_ship(level, point):
            if len(self.stack_ships) > 0:
                size_necessary_ship = self.stack_ships.pop()
                possible_ship = self.get_possible_ship_subject_to_axis(
                                size_necessary_ship, point, 'x')
                possible = self.check_possibility_of_placing_the_ship(
                           level, possible_ship)
                if not possible:
                    possible_ship \
                        = self.get_possible_ship_subject_to_axis(
                          size_necessary_ship, point, 'y')
                    possible \
                        = self.check_possibility_of_placing_the_ship(
                          level, possible_ship)
                if possible:
                    self.add_ship_on_field(level, possible_ship)
                else:
                    self.stack_ships.append(size_necessary_ship)
        else:
            if activate_del:
                x, y = point
                axis = self.determine_axis(level, point)
                size_current_ship = self.field_for_ships[level][x][y]
                current_ship = self.find_ship_on_the_field(level, axis, point, size_current_ship)
                self.delete_ship(level, current_ship)
                self.stack_ships.append(size_current_ship)
            else:
                x, y = point
                if self.field_for_ships[level][x][y] != 1:
                    reverse_axes = {'x': 'y', 'y': 'x'}
                    axis = self.determine_axis(level, point)
                    reverse_axis = reverse_axes[axis]
                    size_current_ship = self.field_for_ships[level][x][y]

                    current_ship = self.find_ship_on_the_field(level, axis, point, size_current_ship)
                    self.delete_ship(level, current_ship)

                    possible_ship = self.get_possible_ship_subject_to_axis(size_current_ship, point, reverse_axis)
                    possibility = self.check_possibility_of_placing_the_ship(level, possible_ship)
                    if possibility:
                        self.add_ship_on_field(level, possible_ship)
                    else:
                        self.add_ship_on_field(level, current_ship)
        self.update_number_of_ships()

    def delete_ship(self, level: int, ship: []) -> None:
        for point in ship:
            x, y = point
            self.field_for_ships[level][x][y] = 0
            self.arrange_the_ships_window.update_buttons_text(level, x, y, '')

    def find_ship_on_the_field(self, level: int, axis: str, point: (int, int), ship_size: int):
        ship = []
        first_point = point
        if axis == 'x':
            while self.is_a_ship(level, first_point):
                if first_point[0] - 1 < 0:
                    break
                first_point = first_point[0] - 1, first_point[1]
            for i in range(ship_size):
                point = first_point[0] + 1 + i, first_point[1]
                ship.append(point)
        else:
            while self.is_a_ship(level, first_point):
                if first_point[1] - 1 < 0:
                    break
                first_point = first_point[0], first_point[1] - 1
            for i in range(ship_size):
                point = first_point[0], first_point[1] + 1 + i
                ship.append(point)
        return ship

    def determine_axis(self, level: int, point: (int, int)) -> str:
        x, y = point
        neighbors = {
            'x': [(x - 1, y), (x + 1, y)],
            'y': [(x, y - 1), (x, y + 1)]
        }
        for axis in neighbors.keys():
            for option in neighbors[axis]:
                if 0 <= option[0] <= self.field_size[0] - 1 and 0 <= option[1] <= self.field_size[1] - 1:
                    if self.is_a_ship(level, option):
                        return axis

    def is_a_ship(self, level: int, point: (int, int)) -> bool:
        x, y = point
        return self.field_for_ships[level][x][y]

    def add_ship_on_field(self, level: int, ship: list) -> None:
        for point in ship:
            x, y = point
            self.field_for_ships[level][x][y] = len(ship)
            self.arrange_the_ships_window.update_buttons_text(level, x, y, str(len(ship)))

    @staticmethod
    def get_possible_ship_subject_to_axis(size_current_ship: int, point: (int, int), axis: str) -> list:
        x, y = point
        possible_ship = []
        for i in range(size_current_ship):
            if axis == 'x':
                possible_ship.append((x + i, y))
            if axis == 'y':
                possible_ship.append((x, y + i))
        return possible_ship

    def check_possibility_of_placing_the_ship(self, level: int, ship: []) -> bool:
        for point in ship:
            x = point[0]
            y = point[1]
            if x not in self.field_for_ships[level].keys() or \
                    y not in self.field_for_ships[level][x].keys() or \
                    self.field_for_ships[level][x][y] != 0:
                return False

        start_x = max(0, ship[0][0] - 1)
        start_y = max(0, ship[0][1] - 1)
        end_x = min(self.field_size[0] - 1, ship[-1][0] + 1)
        end_y = min(self.field_size[1] - 1, ship[-1][1] + 1)
        result = self.checking_the_placement_area(level, start_x, start_y, end_x, end_y)
        return result

    def checking_the_placement_area(self, level: int, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        result = False
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if x in self.field_for_ships[level].keys() and \
                        y in self.field_for_ships[level][x].keys() and \
                        self.field_for_ships[level][x][y] == 0:
                    result = True
                else:
                    return False
        return result

    def create_start_field_for_ships(self) -> dict:
        start_field = {0: {}, 1: {}}
        for x in range(self.field_size[0]):
            start_field[0][x] = {}
            if self.three_dimensional:
                start_field[1][x] = {}
            for y in range(self.field_size[1]):
                start_field[0][x][y] = 0
                if self.three_dimensional:
                    start_field[1][x][y] = 0
        return start_field

    def create_an_environment(self):
        self.create_window()

        number_of_cells = self.field_size[0] * self.field_size[1]
        if self.three_dimensional:
            number_of_cells = number_of_cells * 2
        data = self.calculate_the_number_of_ships_on_the_field(number_of_cells)
        self.fill_stack_ships(data)
        self.update_number_of_ships()

    def create_window(self):
        self.arrange_the_ships_window \
            = ArrangeTheShipsWindow(self.field_size, self.three_dimensional)
        self.arrange_the_ships_window.establish_communication(
            self.processing_options_for_the_location_of_the_ship)
        self.arrange_the_ships_window.setupUi()
        self.arrange_the_ships_window.show()

    def fill_stack_ships(self, data_about_number_of_ships: dict):
        for ship in reversed(data_about_number_of_ships.keys()):
            self.stack_ships.extend(repeat(ship, data_about_number_of_ships[ship]))

    def update_number_of_ships(self):
        template_data = collections.Counter({4: 0, 3: 0, 2: 0, 1: 0})
        new_data_about_ship_number = collections.Counter(self.stack_ships)
        new_data_about_ship_number.update(template_data)
        self.arrange_the_ships_window.update_info_on_label(new_data_about_ship_number)

    @staticmethod
    def calculate_the_number_of_ships_on_the_field(number_of_cells: int) -> dict:
        number_of_cells_for_ships = number_of_cells // 5
        multiplicity = number_of_cells_for_ships // 20
        number_of_ships = {
            4: 1 * multiplicity,
            3: 2 * multiplicity,
            2: 3 * multiplicity,
            1: 4 * multiplicity
        }
        return number_of_ships
