from copy import copy
from typing import Dict, Tuple, List


from objects.ai import AI
from objects.player import Player
from objects.ship import Ship
from windows.game_window import GameWindow
from work_with_confg.config_handler import ConfigHandler


class Game:
    def __init__(self, one_field_size: [int], three_dimensional: bool,
                 player_ships: List[Ship], number_of_ships_per_level: Dict[int, int], ai_level: str):
        self.one_field_size = one_field_size
        self.three_dimensional = three_dimensional
        self.ai_level: str = ai_level
        self.game_window = None
        self.create_window()

        self.game_is_over = False
        self.now_the_player_turn = True

        self.number_of_enemy_ships_first_level = {}
        self.number_of_enemy_ships_second_level = {}

        self.activity_on_player_field: Dict[Tuple[int, Tuple[int, int]], str] = {}
        self.activity_on_enemy_field: Dict[Tuple[int, Tuple[int, int]], str] = {}
        self.record_player_primary_activity(player_ships=player_ships)

        self.number_of_enemy_ships_first_level \
            = copy(number_of_ships_per_level)
        if self.three_dimensional:
            self.number_of_enemy_ships_second_level \
                = copy(number_of_ships_per_level)

        self.player = Player(player_ships)

        self.game_window.display_all_player_ship(player_ships)

        config_parser = ConfigHandler()
        self.hits_statuses = config_parser.read_config_file('hits_statuses')

        self.enemy = AI(one_field_size, self.three_dimensional, ai_level)
        self.enemy.establish_communication(self.enemy_shot_handler)
        self.update_info_data_about_destroyed_ships()

    def record_player_primary_activity(self, player_ships: List[Ship]) -> None:
        for ship in player_ships:
            level = ship.level
            for point in ship.position:
                key = (level, point)
                self.activity_on_player_field[key] = 1

    def shot_handler(self, unit: str, level: int, point: (int, int)):
        if unit == 'enemy':
            response, ship_or_none_if_its_not_kill \
                = self.enemy.process_a_shot(level, point)
        else:
            response, ship_or_none_if_its_not_kill \
                = self.player.process_a_shot(level, point)
        if response == self.hits_statuses['wound']:
            self.react_to_wound(unit=unit, level=level, point=point)
        elif response == self.hits_statuses['kill']:
            self.react_to_kill(
                unit=unit, level=level, point=point,
                ship=ship_or_none_if_its_not_kill)
        elif response == self.hits_statuses['fluffed']:
            self.react_to_fluffed(unit=unit, level=level, point=point)
        self.game_is_over \
            = not self.enemy.live_ships_remained() \
            or not self.player.live_ships_remained()
        if self.game_is_over:
            self.finish_the_game(loser=unit)
        return response, ship_or_none_if_its_not_kill

    def react_to_wound(self, unit: str, level: int, point: Tuple[int, int]) -> None:
        self.display_shot(unit=unit, level=level, point=point, hit_the_ship=True)
        self.record_the_shots(unit=unit, level=level, point=point,
                              points_around_perimeter=[], hit_the_ship=True)

    def react_to_kill(
            self, unit: str, level: int,
            point: Tuple[int, int],
            ship: List[Tuple[int, int]]) -> None:
        who_fired: str = self.find_the_shooter(who_was_hit=unit)
        points_around_perimeter: List[Tuple[int, int]] = []
        if who_fired == 'player' or (who_fired == 'enemy' and self.ai_level != 'very easy'):
            points_around_perimeter = self.find_points_around_perimeter(ship=ship)
        self.display_destroyed_ship(
            unit=unit, level=level, last_hit_on_the_ship=point,
            points_around_perimeter=points_around_perimeter)
        self.record_the_shots(
            unit=unit, level=level, point=point,
            points_around_perimeter=points_around_perimeter, hit_the_ship=True)

    def react_to_fluffed(self, unit: str, level: int, point: Tuple[int, int]):
        self.display_shot(unit=unit, level=level, point=point, hit_the_ship=False)
        self.record_the_shots(unit=unit, level=level, point=point,
                              points_around_perimeter=[], hit_the_ship=False)

    def record_the_shots(
            self, unit: str, level: int, point: Tuple[int, int],
            points_around_perimeter: List[Tuple[int, int]],
            hit_the_ship: bool) -> None:
        field_of_the_victim = (
            self.activity_on_player_field if unit == 'player'
            else self.activity_on_enemy_field)
        key = (level, point)
        if hit_the_ship:
            field_of_the_victim[key] = '0'
            for point in points_around_perimeter:
                key_perimeter_point = (level, point)
                field_of_the_victim[key_perimeter_point] = '#'
        else:
            field_of_the_victim[key] = '#'

    @staticmethod
    def find_the_shooter(who_was_hit: str) -> str:
        opposite_parties = {
            'player': 'enemy',
            'enemy': 'player'
        }
        who_fired = opposite_parties[who_was_hit]
        return who_fired

    def display_destroyed_ship(
            self, unit: str, level: int, last_hit_on_the_ship: Tuple[int, int],
            points_around_perimeter: List[Tuple[int, int]]) -> None:
        self.display_the_area_hits(unit=unit, level=level, points=points_around_perimeter)
        self.display_shot(unit=unit, level=level, point=last_hit_on_the_ship, hit_the_ship=True)

    def display_the_area_hits(self, unit: str, level: int, points: List[Tuple[int, int]]) -> None:
        for point in points:
            self.display_shot(unit=unit, level=level, point=point, hit_the_ship=False)

    def display_shot(self, unit: str, level: int, point: Tuple[int, int], hit_the_ship: bool) -> None:
        self.game_window.display_a_hit(unit=unit, level=level, point=point, fluff=not hit_the_ship)

    def find_points_around_perimeter(
            self, ship: List[Tuple[int, int]]) \
            -> List[Tuple[int, Tuple[int, int]]]:
        points_around_perimeter: List[Tuple[int, Tuple[int, int]]] = []
        start_x = max(0, ship[0][0] - 1)
        start_y = max(0, ship[0][1] - 1)
        end_x = min(self.one_field_size[0] - 1, ship[-1][0] + 1)
        end_y = min(self.one_field_size[1] - 1, ship[-1][1] + 1)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if (x, y) not in ship:
                    points_around_perimeter.append((x, y))
        return points_around_perimeter

    def finish_the_game(self, loser: str) -> None:
        opposite_parties = {
            'player': 'enemy',
            'enemy': 'player'
        }
        winner = opposite_parties[loser]
        self.game_window.display_game_is_over_caption(winner)

        self.enemy.stopwatch_for_ai.stop()

    def update_info_data_about_destroyed_ships(self) -> None:
        self.game_window.update_info_on_label(
            self.number_of_enemy_ships_first_level,
            self.number_of_enemy_ships_second_level)

    def update_info_about_current_situation_on_game(
            self, whose_turn: str, last_shooter: str,
            level: int, point: Tuple[int, int]) -> None:
        self.game_window\
            .update_text_on_label_with_info_about_the_course_of_the_game(
             whose_turn, last_shooter, level, point)

    def player_shot_handler(self, level: int, point: Tuple[int, int]):
        if not self.game_is_over:
            if self.now_the_player_turn:
                response, output = self.shot_handler('enemy', level, point)
                if output is not None:
                    ship_length = len(output)
                    if level == 0:
                        self.number_of_enemy_ships_first_level[
                            ship_length] -= 1
                    else:
                        self.number_of_enemy_ships_second_level[
                            ship_length] -= 1
                    self.update_info_data_about_destroyed_ships()
                self.change_the_turn('enemy')
                self.update_info_about_current_situation_on_game(
                    'enemy', 'player', level, point)

    def enemy_shot_handler(self, level: int, point: Tuple[int, int]):
        if not self.game_is_over:
            if not self.now_the_player_turn:
                response, output = self.shot_handler('player', level, point)
                self.change_the_turn('player')
                self.update_info_about_current_situation_on_game(
                    'player', 'enemy', level, point)
                return response, output

    def change_the_turn(self, who_goes_there: str):
        result = who_goes_there == 'player'
        self.now_the_player_turn = result
        self.enemy.now_my_turn = not self.now_the_player_turn

    def get_actual_info_about_activity_on_fields(self):
        return self.activity_on_player_field, self.activity_on_enemy_field

    def create_window(self):
        self.game_window = GameWindow(
            self.one_field_size, self.three_dimensional)
        self.game_window.establish_connection(
            self.player_shot_handler,
            self.get_actual_info_about_activity_on_fields)
        self.game_window.setupUi()
        self.game_window.show()
