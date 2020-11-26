from functools import partial
from typing import Dict, List, Tuple

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from windows.window_create_helper import WindowCreateHelper
from work_with_confg.config_handler import ConfigHandler


class GameWindow(QMainWindow):
    def __init__(self, one_field_size: [], three_dimensional: bool):
        super().__init__()
        self.config_parser = ConfigHandler()
        self.window_create_helper = WindowCreateHelper()
        self.one_field_size = one_field_size
        self.three_dimensional = three_dimensional

        self.player_shot_handler = None

        self.player_buttons: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] = None
        self.enemy_buttons: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] = None
        self.button_to_change_level: QtWidgets.QPushButton = None

        self.labels_first_lvl: List[QtWidgets.QLabel] = None
        self.labels_second_lvl: List[QtWidgets.QLabel] = None

        self.current_level: int = 0
        self.interval_x: Tuple[int, int] \
            = (0, 15) if self.one_field_size[0] >= 15 else (0, 9)
        self.interval_y: Tuple[int, int] \
            = (0, 15) if self.one_field_size[1] >= 15 else (0, 9)

        self.labels_for_display_interval: Dict[str, QtWidgets.QLabel] = None
        self.label_with_info_about_the_course_of_the_game: QtWidgets.QLabel \
            = None
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

        self.label_with_info_about_the_course_of_the_game \
            = self.create_label_with_info_about_the_course_of_the_game()
        self.final_caption_labels = self.game_is_over_label_create()
        self.labels_first_lvl, self.labels_second_lvl \
            = self.create_inscriptions()
        if self.one_field_size[0] > 16:
            self.create_direction_arrows_button()
            self.labels_for_display_interval \
                = self.create_labels_with_intervals()
            self.update_labels_with_intervals()
        self.label_fields_first_level, self.label_fields_second_level \
            = self.create_label_fields()

        if self.three_dimensional:
            self.button_to_change_level = self.create_button_to_change_levels()

    def create_labels_with_intervals(self) -> Dict[str, QtWidgets.QLabel]:
        labels: Dict[str, QtWidgets.QLabel] \
            = self.window_create_helper.create_labels_with_intervals(
            self.central_widget, 'label_field_game_window')
        return labels

    def create_direction_arrows_button(self) \
            -> Dict[str, QtWidgets.QPushButton]:
        arrows_button: Dict[str, QtWidgets.QPushButton] = \
            self.window_create_helper.create_direction_arrows_button(
                window='game', central_widget=self.central_widget,
                method_for_make_a_shift_in_the_field=self.make_a_shift_in_the_field)
        return arrows_button

    def make_a_shift_in_the_field(self, direction: str) -> None:
        self.interval_x, self.interval_y, shift_occurred \
            = self.window_create_helper.make_a_shift_in_the_interval(
              direction, self.interval_x, self.interval_y, self.one_field_size)
        if shift_occurred:
            self.hide_all_field_button()
            self.show_area_field_button(
                self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

    def hide_all_field_button(self) -> None:
        self.window_create_helper.hide_all_field_button(
            first_field_button=self.player_buttons, second_field_button=self.enemy_buttons)

    def show_area_field_button(
            self, level: int, area: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        self.window_create_helper.show_area_field_button(
            first_field_button=self.player_buttons,
            second_field_button=self.enemy_buttons,
            level=level, area=area)

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
            = self.config_parser.read_config_file(
              'inscriptions_and_geometric_data_game_window')
        for option_winner in \
                inscriptions_and_geometric_data['end_game'].keys():
            text, geometric_data = list(
                inscriptions_and_geometric_data['end_game']
                [option_winner].items())[0]
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

    def display_all_player_ship(self, ships: []) -> None:
        for ship in ships:
            level = ship.level
            text = str(ship.size)
            for position in ship.position:
                x = position[0]
                y = position[1]
                self.player_buttons[level][x][y].setIcon(QtGui.QIcon('./images/ship.jpg'))

    def update_info_on_label(
            self, data_first_lvl: dict, data_second_lvl: dict) -> None:
        self.window_create_helper.update_info_on_label(
            three_dimensional=self.three_dimensional,
            label_fields_first_level=self.label_fields_first_level,
            label_fields_second_level=self.label_fields_second_level,
            data_first_lvl=data_first_lvl,
            data_second_lvl=data_second_lvl)

    def create_label_fields(self) -> Tuple[Dict[str, QtWidgets.QLabel], Dict[str, QtWidgets.QLabel]]:
        label_fields_first_level, label_fields_second_level \
            = self.window_create_helper.create_label_fields(
              config_name='label_field_game_window',
              three_dimensional=self.three_dimensional,
              central_widget=self.central_widget)
        return label_fields_first_level, label_fields_second_level

    def create_inscriptions(self) \
            -> Tuple[List[QtWidgets.QLabel], List[QtWidgets.QLabel]]:
        labels_first_lvl: List[QtWidgets.QLabel] = []
        labels_second_lvl: List[QtWidgets.QLabel] = []
        labels_first_lvl, labels_second_lvl \
            = self.window_create_helper.create_inscriptions(
              self.central_widget,
              three_dimensional=self.three_dimensional,
              config_name='inscriptions_and_geometric_data_game_window')
        return labels_first_lvl, labels_second_lvl

    def create_unchanged_labels(
            self, data: Dict[str, List[int]], hide: bool) -> List[QtWidgets.QLabel]:
        labels: List[QtWidgets.QLabel] \
            = self.window_create_helper.create_unchanged_labels(
            self.central_widget, data, hide=hide)
        return labels

    def create_button_to_change_levels(self) -> QtWidgets.QPushButton:
        geometric_data: Tuple[int, int, int, int] = (220, 30, 260, 70)
        button_to_change_levels \
            = self.window_create_helper.create_button_to_change_levels(
              self.central_widget, self.change_levels, geometric_data)
        return button_to_change_levels

    def change_levels(self, button_to_change_levels: QtWidgets.QPushButton) -> None:
        self.window_create_helper.change_text_level_button(button_to_change_levels)
        result = self.current_level == 0
        self.current_level = 1 if result else 0

        self.change_the_display_of_buttons()
        self.change_the_display_labels(result)

    def change_the_display_labels(self, result: bool):
        self.window_create_helper.change_the_display_labels(
            label_fields_first_level=self.label_fields_first_level,
            label_fields_second_level=self.label_fields_second_level,
            labels_first_lvl=self.labels_first_lvl,
            labels_second_lvl=self.labels_second_lvl, result=result)

    def change_the_display_of_buttons(self) -> None:
        self.window_create_helper.change_the_display_of_buttons(
            first_field_button=self.player_buttons, second_field_button=self.enemy_buttons,
            current_level=self.current_level, interval_x=self.interval_x, interval_y=self.interval_y)

    def change_the_display_changed_labels(
            self, data: Dict[str, QtWidgets.QLabel], show: bool) -> None:
        self.window_create_helper.change_the_display_changed_labels(data, show)

    def change_the_display_unchanged_labels(
            self, data: List[QtWidgets.QLabel], show: bool) -> None:
        self.window_create_helper.change_the_display_unchanged_labels(data, show)

    def create_field_buttons_player(self) \
            -> Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]:
        start_x_player = 40
        buttons = self.create_field_buttons(start_x_player, is_a_player=True)
        return buttons

    def create_field_buttons_enemy(self) \
            -> Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]:
        if self.one_field_size[0] > 15:
            start_x_enemy = 40 + 20 * 16 + 50
        else:
            start_x_enemy = 40 + 20 * 10 + 50
        buttons = self.create_field_buttons(start_x_enemy, is_a_player=False)
        return buttons

    def establish_connection(self, player_shot_handler) -> None:
        self.player_shot_handler = player_shot_handler

    def update_labels_with_intervals(self) -> None:
        self.window_create_helper.update_labels_with_intervals(
            config_name='label_field_game_window', interval_x=self.interval_x,
            interval_y=self.interval_y, labels_for_display_interval=self.labels_for_display_interval)

    @staticmethod
    def get_coordinate_grid(start_x: int) -> Tuple[List[int], List[int]]:
        x_coordinates = []
        y_coordinates = []
        for i in range(16):
            x_coordinates.append(start_x + i * 20)
            y_coordinates.append(178 + i * 20)
        return x_coordinates, y_coordinates

    def create_field_buttons(self, start_x: int, is_a_player: bool) \
            -> Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]:
        coordinate_grid = self.get_coordinate_grid(start_x)
        field: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] \
            = self.window_create_helper.create_field_buttons(
            central_widget=self.central_widget, field_size=self.one_field_size,
            coordinate_grid=coordinate_grid, three_dimensional=self.three_dimensional,
            make_button_active=not is_a_player, method_for_connect_clicked=self.player_shot_handler)
        return field

    def display_a_hit(
            self, unit: str, level: int, point: (int, int), fluf: bool) -> None:
        if unit == 'enemy':
            x, y = point
            if fluf:
                self.enemy_buttons[level][x][y].setIcon(QtGui.QIcon('./images/hit.jpg'))
            else:
                self.enemy_buttons[level][x][y].setIcon(QtGui.QIcon('./images/destroyed_ship.jpg'))
            self.enemy_buttons[level][x][y].setEnabled(False)
        else:
            x, y = point
            if fluf:
                self.player_buttons[level][x][y].setIcon(QtGui.QIcon('./images/hit.jpg'))
            else:
                self.player_buttons[level][x][y].setIcon(QtGui.QIcon('./images/destroyed_ship.jpg'))
            self.player_buttons[level][x][y].setEnabled(False)

    def display_the_destruction(self, unit: str, level: int, ship: [], ai_level: str) -> None:
        opposite_parties = {
            'player': 'enemy',
            'enemy': 'player'
        }
        who_shoot = opposite_parties[unit]

        if who_shoot == 'player' or (who_shoot == 'enemy' and ai_level != 'very easy'):
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
                    field[level][x][y].setIcon(QtGui.QIcon('./images/hit.jpg'))
                    field[level][x][y].setEnabled(False)
        for point in ship:
            self.display_a_hit(unit, level, point, fluf=False)

    def customize_window(self):
        window_size = self.calculate_window_size()
        self.window_create_helper.customize_window(self, 'Игра', window_size)

    def calculate_window_size(self) -> Tuple[int, int]:
        width, height = self.window_create_helper.calculate_window_size(
            self.one_field_size, two_field=True)
        return width, height
