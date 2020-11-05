import collections
from copy import copy
from typing import Dict, Tuple

from PyQt5 import QtCore

from objects.ai import AI
from objects.player import Player
from windows.game_window import GameWindow


class Game:
    def __init__(self, one_field_size: [int], three_dimensional: bool,
                 player_ships: [], number_of_ships_per_level: Dict[int, int]):
        self.one_field_size = one_field_size
        self.three_dimensional = three_dimensional
        self.game_window = None
        self.create_window()

        self.game_is_over = False
        self.now_the_player_turn = True

        self.number_of_enemy_ships_first_level = {}
        self.number_of_enemy_ships_second_level = {}

        self.number_of_enemy_ships_first_level \
            = copy(number_of_ships_per_level)
        if self.three_dimensional:
            self.number_of_enemy_ships_second_level \
                = copy(number_of_ships_per_level)

        self.stopwatch_for_ai = self.create_stopwatch()
        self.stopwatch_time = QtCore.QTime(0, 0, 0)
        self.stopwatch_for_ai.start(1000)

        self.player = Player(player_ships)

        self.game_window.display_all_player_ship(player_ships)

        self.enemy = AI(one_field_size, self.three_dimensional)
        self.update_info_data_about_destroyed_ships()

    def create_stopwatch(self) -> QtCore.QTimer:
        stopwatch = QtCore.QTimer()
        stopwatch.timeout.connect(self.stopwatch_event)
        return stopwatch

    def stopwatch_event(self) -> None:
        level, point = self.enemy.do_shoot()
        output = self.enemy_shot_handler(level, point)
        if output is not None:
            self.enemy.update_used_cells(output)

    def shot_handler(self, unit: str, level: int, point: (int, int)):
        if unit == 'enemy':
            response, ship_or_none_if_its_not_kill \
                = self.enemy.process_a_shot(level, point)
        else:
            response, ship_or_none_if_its_not_kill \
                = self.player.process_a_shot(level, point)
        if response == 'wound':
            self.game_window.display_a_hit(unit, level, point, fluf=False)
        elif response == 'kill':
            self.game_window.display_the_destruction(
                unit, level, ship_or_none_if_its_not_kill)
        elif response == 'fluffed':
            self.game_window.display_a_hit(unit, level, point, fluf=True)
        self.game_is_over \
            = not self.enemy.live_ships_remained() \
            or not self.player.live_ships_remained()
        if self.game_is_over:
            self.finish_the_game(loser=unit)
        return ship_or_none_if_its_not_kill

    def finish_the_game(self, loser: str) -> None:
        opposite_parties = {
            'player': 'enemy',
            'enemy': 'player'
        }
        winner = opposite_parties[loser]
        self.game_window.display_game_is_over_caption(winner)
        self.stopwatch_for_ai.stop()

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

    def player_shot_handler(self, level: int, point: (int, int)):
        if not self.game_is_over:
            if self.now_the_player_turn:
                output = self.shot_handler('enemy', level, point)
                if output is not None:
                    ship_length = len(output)
                    if level == 0:
                        self.number_of_enemy_ships_first_level[
                            ship_length] -= 1
                    else:
                        self.number_of_enemy_ships_second_level[
                            ship_length] -= 1
                    self.update_info_data_about_destroyed_ships()
                self.now_the_player_turn = False
                self.update_info_about_current_situation_on_game(
                    'enemy', 'player', level, point)

    def enemy_shot_handler(self, level: int, point: (int, int)):
        if not self.game_is_over:
            if not self.now_the_player_turn:
                output = self.shot_handler('player', level, point)
                self.now_the_player_turn = True
                self.update_info_about_current_situation_on_game(
                    'player', 'enemy', level, point)
                return output

    def create_window(self):
        self.game_window = GameWindow(
            self.one_field_size, self.three_dimensional)
        self.game_window.establish_connection(self.player_shot_handler)
        self.game_window.setupUi()
        self.game_window.show()
