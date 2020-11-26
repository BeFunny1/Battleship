import collections
from itertools import repeat
from typing import Dict, Tuple, List

from windows.arrange_the_ships_window import ArrangeTheShipsWindow


class ArrangeTheShipsLogic:
    def __init__(self, field_size: Tuple[int, int],
                 three_dimensional: bool, for_test: bool):
        self.for_test: bool = for_test
        self.field_size: Tuple[int, int] = field_size
        self.three_dimensional: bool = three_dimensional
        self.arrange_the_ships_window = None
        self.field_for_related_entity = None
        self.number_of_ships_per_level: Dict[int, int] = {}
        self.stack_related_entity_first_lvl: List[int] = []
        self.stack_related_entity_second_lvl: List[int] = []

        self.customer = None
        if not for_test:
            self.create_an_environment()

    def processing_options_for_the_location_of_the_ship(
            self, level: int, point: Tuple[int, int]) -> None:
        if not self.for_test:
            activate_del = self.arrange_the_ships_window.button_del_activity
        else:
            activate_del = False

        if not self.is_a_related_entity(level, point):
            if not self.all_ships_arrange():
                if self.user_can_pick_this_cell(level):
                    self.related_entity_placement(level, point)
        else:
            if activate_del:
                self.delete_related_entity(level, point)
            else:
                self.try_to_change_related_entity_axis(level, point)

        if not self.for_test:
            self.update_number_of_related_entity()
            allow = self.all_ships_arrange()
            self.open_possibility_of_start_the_game(allow=allow)

    def user_can_pick_this_cell(self, level: int) -> bool:
        if level == 0:
            return len(self.stack_related_entity_first_lvl) > 0
        else:
            return len(self.stack_related_entity_second_lvl) > 0

    def all_ships_arrange(self) -> bool:
        return len(self.stack_related_entity_first_lvl) == 0 \
               and len(self.stack_related_entity_second_lvl) == 0

    def open_possibility_of_start_the_game(self, allow: bool) -> None:
        self.arrange_the_ships_window.switch_start_game_button(allow)

    def go_to_the_next_stage(self) -> None:
        information_about_all_related_entity \
            = self.get_information_about_all_related_entity()
        self.customer(information_about_all_related_entity,
                      self.number_of_ships_per_level)

    def hide_window(self) -> None:
        self.arrange_the_ships_window.hide()

    def establish_communication(self, customer) -> None:
        self.customer = customer

    def get_information_about_all_related_entity(self) -> List[Tuple[int, Tuple[int, int]]]:
        information = []
        for level in self.field_for_related_entity.keys():
            for x in self.field_for_related_entity[level]:
                for y in self.field_for_related_entity[level][x]:
                    if self.is_a_related_entity(level, (x, y)):
                        axis = self.determine_axis(level, (x, y))
                        related_entity_size \
                            = self.field_for_related_entity[level][x][y]
                        related_entity = self.find_related_entity_on_the_field(
                            level, axis, (x, y), related_entity_size)
                        information.append((level, related_entity))
                        self.erase_the_related_entity_from_the_field(
                            level, related_entity)
        return information

    def try_to_change_related_entity_axis(self, level: int, point: Tuple[int, int]) -> None:
        x, y = point
        if self.field_for_related_entity[level][x][y] != 1:
            reverse_axes = {'x': 'y', 'y': 'x'}
            axis = self.determine_axis(level, point)
            reverse_axis = reverse_axes[axis]
            size_current_related_entity \
                = self.field_for_related_entity[level][x][y]

            current_related_entity = self.find_related_entity_on_the_field(
                level, axis, point, size_current_related_entity)
            self.erase_the_related_entity_from_the_field(
                level, current_related_entity)

            possible_related_entity \
                = self.get_possible_related_entity_subject_to_axis(
                    size_current_related_entity, point, reverse_axis)
            possibility \
                = self.check_possibility_of_placing_the_related_entity(
                    level, possible_related_entity)
            if possibility:
                self.add_related_entity_on_field(
                    level, possible_related_entity)
            else:
                self.add_related_entity_on_field(
                    level, current_related_entity)

    def delete_related_entity(self, level: int, point: (int, int)) -> None:
        x, y = point
        axis = self.determine_axis(level, point)
        size_current_related_entity \
            = self.field_for_related_entity[level][x][y]
        current_related_entity \
            = self.find_related_entity_on_the_field(
                level, axis, point, size_current_related_entity)
        self.erase_the_related_entity_from_the_field(
            level, current_related_entity)
        if level == 0:
            self.stack_related_entity_first_lvl.append(
                size_current_related_entity)
        else:
            self.stack_related_entity_second_lvl.append(
                size_current_related_entity)

    def related_entity_placement(self, level: int, point: (int, int)) -> None:
        if level == 0:
            size_necessary_related_entity \
                = self.stack_related_entity_first_lvl.pop()
        else:
            size_necessary_related_entity \
                = self.stack_related_entity_second_lvl.pop()
        possible_related_entity \
            = self.get_possible_related_entity_subject_to_axis(
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
            if level == 0:
                self.stack_related_entity_first_lvl.append(
                    size_necessary_related_entity)
            else:
                self.stack_related_entity_second_lvl.append(
                    size_necessary_related_entity)

    def erase_the_related_entity_from_the_field(
            self, level: int, related_entity: []) -> None:
        for point in related_entity:
            x, y = point
            self.field_for_related_entity[level][x][y] = 0
            if not self.for_test:
                self.arrange_the_ships_window.update_buttons_text(
                    level, x, y, '')

    def find_related_entity_on_the_field(
            self, level: int, axis: str,
            point: Tuple[int, int], related_entity_size: int) -> List[Tuple[int, int]]:
        related_entity = []
        first_point = point
        if axis == 'x':
            while True:
                if first_point[0] - 1 < 0 or not self.is_a_related_entity(
                        level, (first_point[0] - 1, first_point[1])):
                    break
                else:
                    first_point = first_point[0] - 1, first_point[1]
            for i in range(related_entity_size):
                point = first_point[0] + i, first_point[1]
                related_entity.append(point)
        else:
            while True:
                if first_point[1] - 1 < 0 or not self.is_a_related_entity(
                        level, (first_point[0], first_point[1] - 1)):
                    break
                else:
                    first_point = first_point[0], first_point[1] - 1
            for i in range(related_entity_size):
                point = first_point[0], first_point[1] + i
                related_entity.append(point)
        return related_entity

    def determine_axis(self, level: int, point: (int, int)) -> str:
        standard_axis = 'x'
        x, y = point
        neighbors = {
            'x': [(x - 1, y), (x + 1, y)],
            'y': [(x, y - 1), (x, y + 1)]
        }
        for axis in neighbors.keys():
            for option in neighbors[axis]:
                if 0 <= option[0] <= self.field_size[0] - 1 \
                        and 0 <= option[1] <= self.field_size[1] - 1:
                    if self.is_a_related_entity(level, option):
                        return axis
        return standard_axis

    def is_a_related_entity(self, level: int, point: (int, int)) -> bool:
        x, y = point
        return self.field_for_related_entity[level][x][y]

    def add_related_entity_on_field(
            self, level: int, related_entity: list) -> None:
        for point in related_entity:
            x, y = point
            self.field_for_related_entity[level][x][y] = len(related_entity)
            if not self.for_test:
                self.arrange_the_ships_window.update_buttons_text(
                    level, x, y, str(len(related_entity)))

    @staticmethod
    def get_possible_related_entity_subject_to_axis(
            size_current_related_entity: int,
            point: (int, int), axis: str) -> List[Tuple[int, int]]:
        x, y = point
        possible_related_entity = []
        for i in range(size_current_related_entity):
            if axis == 'x':
                possible_related_entity.append((x + i, y))
            if axis == 'y':
                possible_related_entity.append((x, y + i))
        return possible_related_entity

    def check_possibility_of_placing_the_related_entity(
            self, level: int, related_entity: []) -> bool:
        for point in related_entity:
            x = point[0]
            y = point[1]
            if x not in self.field_for_related_entity[level].keys() \
                    or \
                    y not in self.field_for_related_entity[level][x].keys() \
                    or \
                    self.field_for_related_entity[level][x][y] != 0:
                return False

        start_x = max(0, related_entity[0][0] - 1)
        start_y = max(0, related_entity[0][1] - 1)
        end_x = min(self.field_size[0] - 1, related_entity[-1][0] + 1)
        end_y = min(self.field_size[1] - 1, related_entity[-1][1] + 1)
        result = self.checking_the_placement_area(
            level, start_x, start_y, end_x, end_y)
        return result

    def checking_the_placement_area(
            self, level: int, start_x: int,
            start_y: int, end_x: int, end_y: int) -> bool:
        results = []
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                cell_available \
                    = self.field_for_related_entity[level][x][y] == 0
                results.append(cell_available)
        return all(results)

    def create_start_field_for_related_entity(self) -> Dict[int, Dict[int, Dict[int, int]]]:
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

    def create_an_environment(self) -> None:
        self.field_for_related_entity \
            = self.create_start_field_for_related_entity()
        self.create_window()

        number_of_cells = self.field_size[0] * self.field_size[1]
        self.number_of_ships_per_level \
            = self.calculate_the_number_of_related_entity_on_the_field(
                number_of_cells)
        self.fill_stack_related_entity(self.number_of_ships_per_level)
        self.update_number_of_related_entity()

    def create_window(self):
        self.arrange_the_ships_window \
            = ArrangeTheShipsWindow(self.field_size, self.three_dimensional)
        self.arrange_the_ships_window.establish_communication(
            self.processing_options_for_the_location_of_the_ship,
            self.go_to_the_next_stage)
        self.arrange_the_ships_window.setupUi()
        self.arrange_the_ships_window.show()

    def fill_stack_related_entity(
            self, data_about_number_of_related_entity: Dict[int, int]) -> None:
        for related_entity in reversed(
                list(data_about_number_of_related_entity.keys())):
            self.stack_related_entity_first_lvl.extend(
                repeat(related_entity,
                       data_about_number_of_related_entity[related_entity]))
            if self.three_dimensional:
                self.stack_related_entity_second_lvl.extend(
                    repeat(related_entity,
                           data_about_number_of_related_entity[
                               related_entity]))

    def update_number_of_related_entity(self) -> None:
        template_data = collections.Counter({4: 0, 3: 0, 2: 0, 1: 0})
        new_data_about_related_entity_number_first_lvl \
            = collections.Counter(self.stack_related_entity_first_lvl)
        new_data_about_related_entity_number_first_lvl.update(template_data)

        new_data_about_related_entity_number_second_lvl \
            = collections.Counter(self.stack_related_entity_second_lvl)
        new_data_about_related_entity_number_second_lvl.update(template_data)
        self.arrange_the_ships_window.update_info_on_label(
            new_data_about_related_entity_number_first_lvl,
            new_data_about_related_entity_number_second_lvl)

    @staticmethod
    def calculate_the_number_of_related_entity_on_the_field(
            number_of_cells: int) -> Dict[int, int]:
        number_of_cells_for_related_entity = number_of_cells // 5
        multiplicity = number_of_cells_for_related_entity // 20
        number_of_related_entity = {
            4: 1 * multiplicity,
            3: 2 * multiplicity,
            2: 3 * multiplicity,
            1: 4 * multiplicity
        }
        return number_of_related_entity
