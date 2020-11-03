from PyQt5 import QtCore

from objects.ai import AI
from objects.player import Player
from windows.game_window import GameWindow


class Game:
    def __init__(self, one_field_size: [int], three_dimensional: bool, player_ships: []):
        self.one_field_size = one_field_size
        self.three_dimensional = three_dimensional
        self.game_window = None
        self.create_window()

        self.game_is_over = False
        self.now_the_player_turn = True

        self.stopwatch_for_ai = self.create_stopwatch()
        self.stopwatch_time = QtCore.QTime(0, 0, 0)
        self.stopwatch_for_ai.start(1000)

        self.player = Player(player_ships)

        self.game_window.display_all_player_ship(player_ships)

        self.enemy = AI(one_field_size, self.three_dimensional)

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
            response, ship = self.enemy.process_a_shot(level, point)
        else:
            response, ship = self.player.process_a_shot(level, point)
        if response == 'wound':
            self.game_window.display_a_hit(unit, level, point, fluf=False)
        elif response == 'kill':
            self.game_window.display_the_destruction(unit, level, ship)
        elif response == 'fluffed':
            self.game_window.display_a_hit(unit, level, point, fluf=True)
        self.game_is_over = not self.enemy.live_ships_remained() or not self.player.live_ships_remained()
        if unit == 'player':
            return ship

    def player_shot_handler(self, level: int, point: (int, int)):
        if not self.game_is_over:
            if self.now_the_player_turn:
                self.shot_handler('enemy', level, point)
                self.now_the_player_turn = False

    def enemy_shot_handler(self, level: int, point: (int, int)):
        if not self.game_is_over:
            if not self.now_the_player_turn:
                output = self.shot_handler('player', level, point)
                self.now_the_player_turn = True
                return output

    def create_window(self):
        self.game_window = GameWindow(self.one_field_size, self.three_dimensional)
        self.game_window.establish_connection(self.player_shot_handler)
        self.game_window.setupUi()
        self.game_window.show()
