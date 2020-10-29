import collections
from itertools import repeat

from windows.arrange_the_ships_window import ArrangeTheShipsWindow


class ArrangeTheShipsLogic:
    def __init__(self, field_size: (int, int), three_dimensional: bool):
        self.field_size = field_size
        self.three_dimensional = three_dimensional
        self.arrange_the_ships_window = None
        self.stack_related_entity = []
        self.field_for_related_entity = self.create_start_field_for_related_entity()
        self.create_an_environment()

    def processing_options_for_the_location_of_the_ship(
            self, level: int, point: (int, int)):
        activate_del = self.arrange_the_ships_window.button_del_activity
        if not self.is_a_related_entity(level, point):
            if len(self.stack_related_entity) > 0:
                self.related_entity_placement(level, point)
        else:
            if activate_del:
                self.delete_related_entity(level, point)
            else:
                self.try_to_change_related_entity_axis(level, point)
        self.update_number_of_related_entity()

        allow = len(self.stack_related_entity) == 0
        self.start_the_game(allow=allow)

    def start_the_game(self, allow: bool):
        self.arrange_the_ships_window.switch_start_game_button(allow)

    def try_to_change_related_entity_axis(self, level: int, point: (int, int)):
        x, y = point
        if self.field_for_related_entity[level][x][y] != 1:
            reverse_axes = {'x': 'y', 'y': 'x'}
            axis = self.determine_axis(level, point)
            reverse_axis = reverse_axes[axis]
            size_current_related_entity = self.field_for_related_entity[level][x][y]

            current_related_entity = self.find_related_entity_on_the_field(
                level, axis, point, size_current_related_entity)
            self.erase_the_related_entity_from_the_field(level, current_related_entity)

            possible_related_entity = self.get_possible_related_entity_subject_to_axis(
                size_current_related_entity, point, reverse_axis)
            possibility = self.check_possibility_of_placing_the_related_entity(level, possible_related_entity)
            if possibility:
                self.add_related_entity_on_field(level, possible_related_entity)
            else:
                self.add_related_entity_on_field(level, current_related_entity)

    def delete_related_entity(self, level: int, point: (int, int)):
        x, y = point
        axis = self.determine_axis(level, point)
        size_current_related_entity = self.field_for_related_entity[level][x][y]
        current_related_entity = self.find_related_entity_on_the_field(level, axis, point, size_current_related_entity)
        self.erase_the_related_entity_from_the_field(level, current_related_entity)
        self.stack_related_entity.append(size_current_related_entity)

    def related_entity_placement(self, level: int, point: (int, int)):
        size_necessary_related_entity = self.stack_related_entity.pop()
        possible_related_entity = self.get_possible_related_entity_subject_to_axis(
            size_necessary_related_entity, point, 'x')
        possible = self.check_possibility_of_placing_the_related_entity(
            level, possible_related_entity)
        if not possible:
            possible_related_entity \
                = self.get_possible_related_entity_subject_to_axis(
                  size_necessary_related_entity, point, 'y')
            possible \
                = self.check_possibility_of_placing_the_related_entity(
                  level, possible_related_entity)
        if possible:
            self.add_related_entity_on_field(level, possible_related_entity)
        else:
            self.stack_related_entity.append(size_necessary_related_entity)

    def erase_the_related_entity_from_the_field(self, level: int, related_entity: []) -> None:
        for point in related_entity:
            x, y = point
            self.field_for_related_entity[level][x][y] = 0
            self.arrange_the_ships_window.update_buttons_text(level, x, y, '')

    def find_related_entity_on_the_field(self, level: int, axis: str, point: (int, int), related_entity_size: int):
        related_entity = []
        first_point = point
        if axis == 'x':
            while self.is_a_related_entity(level, first_point):
                if first_point[0] - 1 < 0:
                    break
                first_point = first_point[0] - 1, first_point[1]
            for i in range(related_entity_size):
                point = first_point[0] + 1 + i, first_point[1]
                related_entity.append(point)
        else:
            while self.is_a_related_entity(level, first_point):
                if first_point[1] - 1 < 0:
                    break
                first_point = first_point[0], first_point[1] - 1
            for i in range(related_entity_size):
                point = first_point[0], first_point[1] + 1 + i
                related_entity.append(point)
        return related_entity

    def determine_axis(self, level: int, point: (int, int)) -> str:
        x, y = point
        neighbors = {
            'x': [(x - 1, y), (x + 1, y)],
            'y': [(x, y - 1), (x, y + 1)]
        }
        for axis in neighbors.keys():
            for option in neighbors[axis]:
                if 0 <= option[0] <= self.field_size[0] - 1 and 0 <= option[1] <= self.field_size[1] - 1:
                    if self.is_a_related_entity(level, option):
                        return axis

    def is_a_related_entity(self, level: int, point: (int, int)) -> bool:
        x, y = point
        return self.field_for_related_entity[level][x][y]

    def add_related_entity_on_field(self, level: int, related_entity: list) -> None:
        for point in related_entity:
            x, y = point
            self.field_for_related_entity[level][x][y] = len(related_entity)
            self.arrange_the_ships_window.update_buttons_text(level, x, y, str(len(related_entity)))

    @staticmethod
    def get_possible_related_entity_subject_to_axis(
            size_current_related_entity: int, point: (int, int), axis: str) -> list:
        x, y = point
        possible_related_entity = []
        for i in range(size_current_related_entity):
            if axis == 'x':
                possible_related_entity.append((x + i, y))
            if axis == 'y':
                possible_related_entity.append((x, y + i))
        return possible_related_entity

    def check_possibility_of_placing_the_related_entity(self, level: int, related_entity: []) -> bool:
        for point in related_entity:
            x = point[0]
            y = point[1]
            if x not in self.field_for_related_entity[level].keys() or \
                    y not in self.field_for_related_entity[level][x].keys() or \
                    self.field_for_related_entity[level][x][y] != 0:
                return False

        start_x = max(0, related_entity[0][0] - 1)
        start_y = max(0, related_entity[0][1] - 1)
        end_x = min(self.field_size[0] - 1, related_entity[-1][0] + 1)
        end_y = min(self.field_size[1] - 1, related_entity[-1][1] + 1)
        result = self.checking_the_placement_area(level, start_x, start_y, end_x, end_y)
        return result

    def checking_the_placement_area(self, level: int, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        result = False
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if x in self.field_for_related_entity[level].keys() and \
                        y in self.field_for_related_entity[level][x].keys() and \
                        self.field_for_related_entity[level][x][y] == 0:
                    result = True
                else:
                    return False
        return result

    def create_start_field_for_related_entity(self) -> dict:
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
        data = self.calculate_the_number_of_related_entity_on_the_field(number_of_cells)
        self.fill_stack_related_entity(data)
        self.update_number_of_related_entity()

    def create_window(self):
        self.arrange_the_ships_window \
            = ArrangeTheShipsWindow(self.field_size, self.three_dimensional)
        self.arrange_the_ships_window.establish_communication(
            self.processing_options_for_the_location_of_the_ship)
        self.arrange_the_ships_window.setupUi()
        self.arrange_the_ships_window.show()

    def fill_stack_related_entity(self, data_about_number_of_related_entity: dict):
        for related_entity in reversed(data_about_number_of_related_entity.keys()):
            self.stack_related_entity.extend(repeat(related_entity, data_about_number_of_related_entity[related_entity]))

    def update_number_of_related_entity(self):
        template_data = collections.Counter({4: 0, 3: 0, 2: 0, 1: 0})
        new_data_about_related_entity_number = collections.Counter(self.stack_related_entity)
        new_data_about_related_entity_number.update(template_data)
        self.arrange_the_ships_window.update_info_on_label(new_data_about_related_entity_number)

    @staticmethod
    def calculate_the_number_of_related_entity_on_the_field(number_of_cells: int) -> dict:
        number_of_cells_for_related_entity = number_of_cells // 5
        multiplicity = number_of_cells_for_related_entity // 20
        number_of_related_entity = {
            4: 1 * multiplicity,
            3: 2 * multiplicity,
            2: 3 * multiplicity,
            1: 4 * multiplicity
        }
        return number_of_related_entity
