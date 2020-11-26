from dataclasses import dataclass
from typing import List, Tuple

from PyQt5 import QtCore

from logic.arrange_the_ships_logic import ArrangeTheShipsLogic
from random import randint

from logic.field import Field
from objects.ship import Ship


class AI:
    def __init__(self, field_size: [int], three_dimensional: bool, ai_level: str):
        self.field_size: Tuple[int, int] = field_size
        self.three_dimensional: bool = three_dimensional
        self.ships: List[Ship] = self.place_ships()
        self.where_did_i_shoot: List[Tuple[int, int]] = []
        self.enemy_shot_handler = None
        self.ai_level = ai_level
        self.now_my_turn: bool = False
        self.finishing_off: FinishingOff = FinishingOff(None, None, None, None)

        self.points_in_different_directions: List[Tuple[int, Tuple[int, int]]] = None

        self.stopwatch_for_ai = self.create_stopwatch()
        self.stopwatch_time: QtCore.QTime = QtCore.QTime(0, 0, 0)
        self.stopwatch_for_ai.start(1000)

    def establish_communication(self, action) -> None:
        self.enemy_shot_handler = action

    def create_stopwatch(self) -> QtCore.QTimer:
        stopwatch = QtCore.QTimer()
        stopwatch.timeout.connect(self.time_to_shoot)
        return stopwatch

    def time_to_shoot(self) -> None:
        if self.now_my_turn:
            level, point = self.select_point_for_shot()

            response, output = self.enemy_shot_handler(level, point)

            if self.ai_level != 'very easy':
                self.do_not_shoot_at_neighboring_points_from_the_ship(output, level)

            if self.ai_level == 'normal':
                self.process_the_reaction_to_the_shot(response, level, point)

    def select_point_for_shot(self) -> Tuple[int, Tuple[int, int]]:
        if self.finishing_off.direction == 'unknown':
            level, point = self.points_in_different_directions.pop()
        elif self.finishing_off.direction is not None:
            level, point = self.select_a_point_according_to_the_direction()
        else:
            level, point = self.select_random_point_for_shot()
        return level, point

    def select_a_point_according_to_the_direction(self) -> Tuple[int, Tuple[int, int]]:
        level = self.finishing_off.level
        point = self.make_a_shot_in_the_direction_of(
            self.finishing_off.direction, self.finishing_off.point)
        if not self.check_point_for_validity(self.finishing_off.level, point):
            self.change_direction()
            point = self.make_a_shot_in_the_direction_of(
                self.finishing_off.direction, self.finishing_off.original_point)
        return level, point

    def select_random_point_for_shot(self) -> Tuple[int, Tuple[int, int]]:
        attempt_a_shot = None
        while attempt_a_shot is None:
            attempt_a_shot = self.try_shoot()
        level, point = attempt_a_shot
        return level, point

    def process_the_reaction_to_the_shot(self, response: str, level: int, point: Tuple[int, int]) -> None:
        if response == 'kill':
            self.finishing_off = FinishingOff(None, None, None, None)
            self.points_in_different_directions = None
        elif response == 'wound':
            if self.finishing_off.point is None:
                self.finishing_off = FinishingOff('unknown', level, point, point)
                self.points_in_different_directions \
                    = self.calculate_the_following_points_for_shots(level, point)
            else:
                if self.finishing_off.direction == 'unknown':
                    self.finishing_off.direction = self.define_an_direction_by_two_points(
                        self.finishing_off.point, point)
                self.finishing_off.point = point
        elif response == 'fluffed' and self.finishing_off.direction not in ['unknown', None]:
            self.change_direction()
            self.finishing_off.point = self.finishing_off.original_point

    def do_not_shoot_at_neighboring_points_from_the_ship(self, output, level: int) -> None:
        if output is not None:
            self.update_used_cells(output, level)

    def check_point_for_validity(self, level: int, point: Tuple[int, int]) -> bool:
        return 0 <= point[0] < self.field_size[0] \
               and 0 <= point[1] < self.field_size[1] \
               and (level, point) not in self.where_did_i_shoot

    @staticmethod
    def make_a_shot_in_the_direction_of(
            direction: str, original_point: Tuple[int, int]) -> Tuple[int, int]:
        dependencies = {
            'right': (1, 0),
            'left': (-1, 0),
            'up': (0, -1),
            'down': (0, 1)
        }
        summands = dependencies[direction]
        new_point = original_point[0] + summands[0], original_point[1] + summands[1]
        return new_point

    def change_direction(self) -> None:
        antipodes = {
            'right': 'left',
            'left': 'right',
            'up': 'down',
            'down': 'up'
        }
        self.finishing_off.direction = antipodes[self.finishing_off.direction]

    def calculate_the_following_points_for_shots(
            self, level: int, point: Tuple[int, int]) -> List[Tuple[int, Tuple[int, int]]]:
        points: List[Tuple[int, Tuple[int, int]]] = []
        for element in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_point = point[0] + element[0], point[1] + element[1]
            if self.check_point_for_validity(level, new_point):
                points.append((level, new_point))
        return points

    @staticmethod
    def define_an_direction_by_two_points(
            first_point: Tuple[int, int], second_point: Tuple[int, int]) -> str:
        if first_point[0] < second_point[0]:
            return 'right'
        elif first_point[0] > second_point[0]:
            return 'left'
        elif first_point[1] < second_point[1]:
            return 'down'
        elif first_point[1] > second_point[1]:
            return 'up'

    def place_ships(self) -> List[Ship]:
        handler = ArrangeTheShipsLogic(
            self.field_size, self.three_dimensional, for_test=True)
        number_of_cells = self.field_size[0] * self.field_size[1]
        number_of_ships \
            = handler.calculate_the_number_of_related_entity_on_the_field(
              number_of_cells)
        handler.field_for_related_entity \
            = handler.create_start_field_for_related_entity()
        handler.fill_stack_related_entity(number_of_ships)
        while len(handler.stack_related_entity_first_lvl) > 0 \
                or len(handler.stack_related_entity_second_lvl) > 0:
            level = 0
            if self.three_dimensional:
                level = randint(0, 1)
            x = randint(0, self.field_size[0] - 1)
            y = randint(0, self.field_size[1] - 1)
            handler.processing_options_for_the_location_of_the_ship(
                level, (x, y))
        information_about_all_related_entity \
            = handler.get_information_about_all_related_entity()
        field = Field(information_about_all_related_entity)
        return field.ships

    def process_a_shot(self, level: int, point: (int, int)) -> Tuple[str, List[Tuple[int, int]]]:
        check, index_ship = self.is_a_ship(level, point)
        if check:
            ship = self.ships[index_ship]
            ship.size -= 1
            if ship.size == 0:
                ship.alive = False
                return 'kill', ship.position
            return 'wound', None
        return 'fluffed', None

    def is_a_ship(self, level: int, point: (int, int)) -> Tuple[bool, int]:
        for index, ship in enumerate(self.ships):
            if ship.level == level:
                if point in ship.position:
                    return True, index
        return False, None

    def update_used_cells(self, ship, level: int) -> None:
        start_x = max(0, ship[0][0] - 1)
        start_y = max(0, ship[0][1] - 1)
        end_x = min(self.field_size[0] - 1, ship[-1][0] + 1)
        end_y = min(self.field_size[1] - 1, ship[-1][1] + 1)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if (level, (x, y)) not in self.where_did_i_shoot:
                    self.where_did_i_shoot.append((level, (x, y)))

    def try_shoot(self) -> Tuple[int, Tuple[int, int]]:
        level = 0
        if self.three_dimensional:
            level = randint(0, 1)
        x = randint(0, self.field_size[0] - 1)
        y = randint(0, self.field_size[1] - 1)
        if (level, (x, y)) not in self.where_did_i_shoot:
            self.where_did_i_shoot.append((level, (x, y)))
            return level, (x, y)

    def live_ships_remained(self) -> bool:
        for ship in self.ships:
            if ship.alive:
                return True
        return False


@dataclass
class FinishingOff:
    direction: str
    level: int
    original_point: Tuple[int, int]
    point: Tuple[int, int]
