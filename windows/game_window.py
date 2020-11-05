from functools import partial
from typing import Dict, List, Tuple

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from work_with_confg.config_handler import ConfigHandler


class GameWindow(QMainWindow):
    def __init__(self, one_field_size: [], three_dimensional: bool):
        super().__init__()
        self.config_reader = ConfigHandler()
        self.one_field_size = one_field_size
        self.three_dimensional = three_dimensional
        self.player_buttons = None
        self.enemy_buttons = None
        self.button_to_change_level = None
        self.labels_field = None
        self.player_shot_handler = None
        self.labels_first_lvl = None
        self.labels_second_lvl = None

        self.current_level: int = 0
        self.interval_x: Tuple[int, int] = (0, 15)
        self.interval_y: Tuple[int, int] = (0, 15)

        self.labels_for_display_interval = None
        self.label_with_info_about_the_course_of_the_game: QtWidgets.QLabel = None
        self.final_caption_labels: Dict[str, QtWidgets.QLabel] = {}
        self.label_fields_first_level: Dict[str, QtWidgets.QLabel] = {}
        self.label_fields_second_level: Dict[str, QtWidgets.QLabel] = {}

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

    def setupUi(self) -> None:
        self.customize_window()
        self.player_buttons = self.create_field_buttons_player()
        self.enemy_buttons = self.create_field_buttons_enemy()

        self.label_with_info_about_the_course_of_the_game = self.create_label_with_info_about_the_course_of_the_game()
        self.final_caption_labels = self.game_is_over_label_create()
        self.labels_first_lvl, self.labels_second_lvl = self.create_inscriptions()
        if self.one_field_size[0] > 16:
            self.create_direction_arrows_button()
            self.labels_for_display_interval \
                = self.create_labels_with_intervals()
            self.update_labels_with_intervals()
        self.label_fields_first_level, self.label_fields_second_level = self.create_label_fields()

        if self.three_dimensional:
            self.button_to_change_level = self.create_button_to_change_levels()

    def create_labels_with_intervals(self):
        data = self.config_reader.read_config_file(
            'label_field_game_window')
        data_for_labels = data['interval']
        labels: Dict[str, QtWidgets.QLabel] = {}
        for key in data_for_labels.keys():
            x, y, width, height = data_for_labels[key]
            label = QtWidgets.QLabel(self.central_widget)
            label.setText(key)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setAlignment(QtCore.Qt.AlignRight)
            if key == 'x_start_player' or key == 'x_start_enemy':
                label.setAlignment(QtCore.Qt.AlignLeft)
            labels[key] = label
        return labels

    def create_direction_arrows_button(self) -> Dict[str, QtWidgets.QPushButton]:
        data_for_buttons = self.config_reader.read_config_file(
            'direction_arrows_button')
        arrows_button: Dict[str, QtWidgets.QPushButton] = {}
        for direction in data_for_buttons.keys():
            text, geometric_data = list(data_for_buttons[direction].items())[0]
            x, y, width, height = geometric_data['game']
            button = QtWidgets.QPushButton(self.central_widget)
            button.setGeometry(QtCore.QRect(x, y, width, height))
            button.setObjectName(f'arrows_button_{direction}')
            button.setText(text)
            button.clicked.connect(partial(self.make_a_shift_in_the_field, direction))
            arrows_button[direction] = button
        return arrows_button

    def make_a_shift_in_the_field(self, direction: str) -> None:
        if direction == 'right' and self.interval_x[1] < self.one_field_size[0] - 1:
            self.hide_all_field_button()
            self.interval_x = self.interval_x[0] + 16, self.interval_x[1] + 16
            self.show_area_field_button(self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

        elif direction == 'left' and self.interval_x[0] > 0:
            self.hide_all_field_button()
            self.interval_x = self.interval_x[0] - 16, self.interval_x[1] - 16
            self.show_area_field_button(self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

        elif direction == 'up' and self.interval_y[0] > 0:
            self.hide_all_field_button()
            self.interval_y = self.interval_y[0] - 16, self.interval_y[1] - 16
            self.show_area_field_button(self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

        elif direction == 'down' and self.interval_y[1] < self.one_field_size[1] - 1:
            self.hide_all_field_button()
            self.interval_y = self.interval_y[0] + 16, self.interval_y[1] + 16
            self.show_area_field_button(self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

    def hide_all_field_button(self) -> None:
        for level in self.player_buttons.keys():
            for x in self.player_buttons[level]:
                for y in self.player_buttons[level][x]:
                    self.player_buttons[level][x][y].hide()
                    self.enemy_buttons[level][x][y].hide()

    def show_area_field_button(self, level: int, area: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        x_start, x_end = area[0]
        y_start, y_end = area[1]
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.player_buttons[level][x][y].show()
                self.enemy_buttons[level][x][y].show()

    def create_label_with_info_about_the_course_of_the_game(self) -> QtWidgets.QLabel:
        text = 'Текущий ход: player. Последний выстрел: , уровень: , точка: '
        x, y, width, height = [0, 120, self.width(), 20]
        label = QtWidgets.QLabel(self.central_widget)
        label.setText(text)
        label.setGeometry(QtCore.QRect(x, y, width, height))
        label.setObjectName("label")
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def update_text_on_label_with_info_about_the_course_of_the_game(
            self, whose_turn: str, last_shooter: str,
            level: int, point: Tuple[int, int]) -> None:
        new_text = f'Текущий ход: {whose_turn}. ' \
                   f'Последний выстрел: {last_shooter}, ' \
                   f'уровень: {str(level)}, ' \
                   f'точка: {str(point)}'
        self.label_with_info_about_the_course_of_the_game.setText(new_text)

    def game_is_over_label_create(self) -> Dict[str, QtWidgets.QLabel]:
        labels: Dict[str, QtWidgets.QLabel] = {}
        inscriptions_and_geometric_data \
            = self.config_reader.read_config_file(
              'inscriptions_and_geometric_data_game_window')
        for option_winner in inscriptions_and_geometric_data['end_game'].keys():
            text, geometric_data = list(inscriptions_and_geometric_data['end_game'][option_winner].items())[0]
            x, y, width, height = geometric_data
            width = self.width()
            label = QtWidgets.QLabel(self.central_widget)
            label.setText(text)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setAlignment(QtCore.Qt.AlignCenter)
            labels[option_winner] = label
            label.hide()
        return labels

    def display_game_is_over_caption(self, winner: str) -> None:
        self.final_caption_labels[winner].show()

    def display_all_player_ship(self, ships: []):
        for ship in ships:
            level = ship.level
            text = str(ship.size)
            for position in ship.position:
                x = position[0]
                y = position[1]
                self.player_buttons[level][x][y].setText(text)

    def update_info_on_label(self, data_first_lvl: dict, data_second_lvl: dict) -> None:
        translator_first_lvl = {
            4: 'battleship',
            3: 'cruiser',
            2: 'destroyer',
            1: 'boat'
        }
        translator_second_lvl = {
            4: 'nuclear submarine',
            3: 'large submarine',
            2: 'medium submarine',
            1: 'ultra-small submarine'
        }
        for key in data_first_lvl.keys():
            first_text = str(data_first_lvl[key])
            self.label_fields_first_level[translator_first_lvl[key]].setText(first_text)
            if self.three_dimensional:
                second_text = str(data_second_lvl[key])
                self.label_fields_second_level[translator_second_lvl[key]].setText(second_text)

    def create_label_fields(self) -> Dict[str, QtWidgets.QLabel]:
        data_for_fields = self.config_reader.read_config_file(
            'label_field_game_window')
        label_fields_first_level: Dict[str, QtWidgets.QLabel] = {}
        label_fields_second_level: Dict[str, QtWidgets.QLabel] = {}

        label_fields_first_level = \
            self.create_changed_labels(data_for_fields['ships'], hide=False)
        if self.three_dimensional:
            label_fields_second_level = \
                self.create_changed_labels(data_for_fields['submarine'], hide=True)
        return label_fields_first_level, label_fields_second_level

    def create_changed_labels(self, data: Dict[str, List[int]], hide: bool) -> Dict[str, QtWidgets.QLabel]:
        label_fields: Dict[str, QtWidgets.QLabel] = {}
        for ship in data:
            x, y, width, height = data[ship]
            ship_counter = QtWidgets.QLabel(self.central_widget)
            ship_counter.setGeometry(QtCore.QRect(x, y, width, height))
            ship_counter.setAlignment(QtCore.Qt.AlignCenter)
            ship_counter.setObjectName("ship")
            ship_counter.setText('0')
            if hide:
                ship_counter.hide()
            label_fields[ship] = ship_counter
        return label_fields

    def create_inscriptions(self) -> Tuple[List[QtWidgets.QLabel], List[QtWidgets.QLabel]]:
        inscriptions_and_geometric_data \
            = self.config_reader.read_config_file(
             'inscriptions_and_geometric_data_game_window')
        self.create_unchanged_labels(
            inscriptions_and_geometric_data['general_labels'], hide=False)
        labels_first_lvl: List[QtWidgets.QLabel] = []
        labels_second_lvl: List[QtWidgets.QLabel] = []

        labels_first_lvl = self.create_unchanged_labels(
            inscriptions_and_geometric_data['ships'], hide=False)
        if self.three_dimensional:
            labels_second_lvl = self.create_unchanged_labels(
                inscriptions_and_geometric_data['submarine'], hide=True)
        return labels_first_lvl, labels_second_lvl

    def create_unchanged_labels(self, data: Dict[str, List[int]], hide: bool) -> List[QtWidgets.QLabel]:
        labels: List[QtWidgets.QLabel] = []
        for inscription in data:
            x, y, width, height = data[inscription]
            label = QtWidgets.QLabel(self.central_widget)
            label.setText(inscription)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setWordWrap(True)
            if hide:
                label.hide()
            labels.append(label)
        return labels

    def create_button_to_change_levels(self) -> QtWidgets.QPushButton:
        button_to_change_levels = QtWidgets.QPushButton(self.central_widget)
        button_to_change_levels.setGeometry(QtCore.QRect(220, 30, 260, 70))
        button_to_change_levels.setObjectName("button_to_change_levels")
        button_to_change_levels.setText('Перейти на нижний уровень')
        button_to_change_levels.clicked.connect(partial(self.change_levels, button_to_change_levels))
        return button_to_change_levels

    def change_levels(self, button_to_change_levels: QtWidgets.QPushButton) -> None:
        reverse_phrases = {
            'Перейти на нижний уровень': 'Перейти на верхний уровень',
            'Перейти на верхний уровень': 'Перейти на нижний уровень'
        }
        current_text = button_to_change_levels.text()
        new_text = reverse_phrases[current_text]
        button_to_change_levels.setText(new_text)
        # result = self.player_buttons[1][0][0].isHidden()
        result = self.current_level == 0
        if result:
            self.current_level = 1
        else:
            self.current_level = 0

        self.change_the_display_of_buttons()

        self.change_the_display_unchanged_labels(self.labels_second_lvl, show=result)
        self.change_the_display_unchanged_labels(self.labels_first_lvl, show=not result)

        self.change_the_display_changed_labels(self.label_fields_second_level, show=result)
        self.change_the_display_changed_labels(self.label_fields_first_level, show=not result)

    def change_the_display_of_buttons(self) -> None:
        self.hide_all_field_button()
        self.show_area_field_button(self.current_level,
                                    (self.interval_x, self.interval_y))

    @staticmethod
    def change_the_display_changed_labels(data: Dict[str, QtWidgets.QLabel], show: bool) -> None:
        for label in data.keys():
            if show:
                data[label].show()
            else:
                data[label].hide()

    @staticmethod
    def change_the_display_unchanged_labels(data: List[QtWidgets.QLabel], show: bool) -> None:
        for label in data:
            if show:
                label.show()
            else:
                label.hide()

    def create_field_buttons_player(self) -> {}:
        start_x_player = 40
        buttons = self.create_field_buttons(start_x_player, is_a_player=True)
        return buttons

    def create_field_buttons_enemy(self) -> {}:
        start_x_enemy = 40 + 20 * 16 + 50
        buttons = self.create_field_buttons(start_x_enemy, is_a_player=False)
        return buttons

    def establish_connection(self, player_shot_handler):
        self.player_shot_handler = player_shot_handler

    def update_labels_with_intervals(self):
        self.labels_for_display_interval['x_start_player'].setText(str(self.interval_x[0]))
        self.labels_for_display_interval['x_end_player'].setText(str(self.interval_x[1]))
        self.labels_for_display_interval['y_start_player'].setText(str(self.interval_y[0]))
        self.labels_for_display_interval['y_end_player'].setText(str(self.interval_y[1]))

        self.labels_for_display_interval['x_start_enemy'].setText(str(self.interval_x[0]))
        self.labels_for_display_interval['x_end_enemy'].setText(str(self.interval_x[1]))
        self.labels_for_display_interval['y_start_enemy'].setText(str(self.interval_y[0]))
        self.labels_for_display_interval['y_end_enemy'].setText(str(self.interval_y[1]))

    @staticmethod
    def get_coordinate_grid(start_x: int) -> Tuple[List[int], List[int]]:
        x_coordinates = []
        y_coordinates = []
        for i in range(16):
            x_coordinates.append(start_x + i * 20)
            y_coordinates.append(178 + i * 20)
        return x_coordinates, y_coordinates

    def create_field_buttons(self, start_x: int, is_a_player: bool) -> {}:
        field: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] = {0: {}, 1: {}}
        x_coordinate_grid, y_coordinate_grid = self.get_coordinate_grid(start_x)
        for x in range(self.one_field_size[0]):
            field[0][x] = {}
            if self.three_dimensional:
                field[1][x] = {}
            for y in range(self.one_field_size[1]):
                button = QtWidgets.QPushButton(self.central_widget)
                button.setEnabled(not is_a_player)
                x_coordinate, y_coordinate = x_coordinate_grid[x % 16], y_coordinate_grid[y % 16]
                button.setGeometry(x_coordinate, y_coordinate, 20, 20)
                button.setObjectName(f'button_field_{x}_{y}')
                if not is_a_player:
                    button.clicked.connect(
                        partial(self.player_shot_handler, 0, (x, y)))
                field[0][x][y] = button
                if x > 15 or y > 15:
                    button.hide()
                if self.three_dimensional:
                    sublevel_button = QtWidgets.QPushButton(self.central_widget)
                    sublevel_button.setGeometry(x_coordinate, y_coordinate, 20, 20)
                    sublevel_button.setObjectName(f'sublevel_button_field_{x}_{y}')
                    sublevel_button.setEnabled(not is_a_player)
                    sublevel_button.hide()
                    if not is_a_player:
                        sublevel_button.clicked.connect(
                            partial(self.player_shot_handler, 1, (x, y)))
                    field[1][x][y] = sublevel_button
        return field

    def display_a_hit(self, unit: str, level: int, point: (int, int), fluf: bool) -> None:
        if unit == 'enemy':
            x, y = point
            if fluf:
                self.enemy_buttons[level][x][y].setText('*')
            else:
                self.enemy_buttons[level][x][y].setText('#')
            self.enemy_buttons[level][x][y].setEnabled(False)
        else:
            x, y = point
            if fluf:
                self.player_buttons[level][x][y].setText('*')
            else:
                self.player_buttons[level][x][y].setText('#')
            self.player_buttons[level][x][y].setEnabled(False)

    def display_the_destruction(self, unit: str, level: int, ship: []):
        start_x = max(0, ship[0][0] - 1)
        start_y = max(0, ship[0][1] - 1)
        end_x = min(self.one_field_size[0] - 1, ship[-1][0] + 1)
        end_y = min(self.one_field_size[1] - 1, ship[-1][1] + 1)
        if unit == 'player':
            field = self.player_buttons
        else:
            field = self.enemy_buttons
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                field[level][x][y].setText('*')
                field[level][x][y].setEnabled(False)
        for point in ship:
            self.display_a_hit(unit, level, point, fluf=False)

    def customize_window(self):
        window_width, window_height = self.calculate_window_size()
        self.setObjectName('MainWindow')
        self.setWindowTitle('Игра')
        self.resize(window_width, window_height)
        self.setMinimumSize(QtCore.QSize(window_width, window_height))
        self.setMaximumSize(QtCore.QSize(window_width, window_height))

    def calculate_window_size(self) -> (int, int):
        if self.one_field_size[0] > 16:
            return 770, 770
        elif self.one_field_size[0] == 16:
            return 770, 520
        else:
            return 520, 400
