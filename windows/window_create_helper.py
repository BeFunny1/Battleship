from functools import partial
from typing import Tuple, Dict, List

from PyQt5 import QtCore, QtWidgets

from work_with_confg.config_handler import ConfigHandler


class WindowCreateHelper:
    def __init__(self):
        self.config_parser = ConfigHandler()

    @staticmethod
    def customize_window(window, window_name: str, window_size: Tuple[int, int]) -> None:
        window.setObjectName('MainWindow')
        window.setWindowTitle(window_name)
        window.resize(window_size[0], window_size[1])
        window.setMinimumSize(QtCore.QSize(window_size[0], window_size[1]))
        window.setMaximumSize(QtCore.QSize(window_size[0], window_size[1]))

    @staticmethod
    def create_button_to_change_levels(
            central_widget: QtWidgets.QWidget, method_for_change_levels,
            geometric_data: Tuple[int, int, int, int]) -> QtWidgets.QPushButton:
        x, y, width, height = geometric_data
        button_to_change_levels = QtWidgets.QPushButton(central_widget)
        button_to_change_levels.setGeometry(QtCore.QRect(x, y, width, height))
        button_to_change_levels.setObjectName("button_to_change_levels")
        button_to_change_levels.setText('Перейти на нижний уровень')
        button_to_change_levels.clicked.connect(
            partial(method_for_change_levels, button_to_change_levels))
        return button_to_change_levels

    @staticmethod
    def change_the_display_changed_labels(
            data: Dict[str, QtWidgets.QLabel], show: bool) -> None:
        for label in data.keys():
            if show:
                data[label].show()
            else:
                data[label].hide()

    @staticmethod
    def change_the_display_unchanged_labels(
            data: List[QtWidgets.QLabel], show: bool) -> None:
        for label in data:
            if show:
                label.show()
            else:
                label.hide()

    @staticmethod
    def hide_all_field_button(
            first_field_button: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]],
            second_field_button: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]) -> None:
        for level in first_field_button.keys():
            for x in first_field_button[level]:
                for y in first_field_button[level][x]:
                    first_field_button[level][x][y].hide()
                    if second_field_button is not None:
                        second_field_button[level][x][y].hide()

    def create_labels_with_intervals(
            self, central_widget: QtWidgets.QWidget,
            config_file: str) -> Dict[str, QtWidgets.QLabel]:
        data = self.config_parser.read_config_file(config_file)
        data_for_labels = data['interval']
        labels: Dict[str, QtWidgets.QLabel] = {}
        for key in data_for_labels.keys():
            x, y, width, height = data_for_labels[key]
            label = QtWidgets.QLabel(central_widget)
            label.setText(key)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setAlignment(QtCore.Qt.AlignRight)
            if 'x_start' in key:
                label.setAlignment(QtCore.Qt.AlignLeft)
            labels[key] = label
        return labels

    def create_direction_arrows_button(
            self, window: str, central_widget: QtWidgets.QWidget,
            method_for_make_a_shift_in_the_field) -> Dict[str, QtWidgets.QPushButton]:
        data_for_buttons = self.config_parser.read_config_file(
            'direction_arrows_button')
        arrows_button: Dict[str, QtWidgets.QPushButton] = {}
        for direction in data_for_buttons.keys():
            text, geometric_data = list(data_for_buttons[direction].items())[0]
            x, y, width, height = geometric_data[window]
            button = QtWidgets.QPushButton(central_widget)
            button.setGeometry(QtCore.QRect(x, y, width, height))
            button.setObjectName(f'arrows_button_{direction}')
            button.setText(text)
            button.clicked.connect(
                partial(method_for_make_a_shift_in_the_field, direction))
            arrows_button[direction] = button
        return arrows_button

    @staticmethod
    def make_a_shift_in_the_interval(
            direction: str, interval_x: Tuple[int, int],
            interval_y: Tuple[int, int], field_size: Tuple[int, int]) \
            -> Tuple[Tuple[int, int], Tuple[int, int], bool]:
        shift_occurred: bool = False
        if direction == 'right' \
                and interval_x[1] < field_size[0] - 1:
            interval_x = interval_x[0] + 16, interval_x[1] + 16
            shift_occurred = True
        elif direction == 'left' \
                and interval_x[0] > 0:
            interval_x = interval_x[0] - 16, interval_x[1] - 16
            shift_occurred = True
        elif direction == 'up' \
                and interval_y[0] > 0:
            interval_y = interval_y[0] - 16, interval_y[1] - 16
            shift_occurred = True
        elif direction == 'down' \
                and interval_y[1] < field_size[1] - 1:
            interval_y = interval_y[0] + 16, interval_y[1] + 16
            shift_occurred = True
        return interval_x, interval_y, shift_occurred

    def update_labels_with_intervals(
            self, config_name: str,
            interval_x: Tuple[int, int], interval_y: Tuple[int, int],
            labels_for_display_interval: Dict[str, QtWidgets.QLabel]) -> None:
        keys_for_labels: List[str] \
            = list(self.config_parser.read_config_file(config_name)['interval'].keys())
        for key in keys_for_labels:
            axis_interval = interval_x if 'x' in key else interval_y
            start_or_end = 0 if 'start' in key else 1
            labels_for_display_interval[key].setText(str(axis_interval[start_or_end]))

    @staticmethod
    def show_area_field_button(
            first_field_button: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]],
            second_field_button: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]],
            level: int, area: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        x_start, x_end = area[0]
        y_start, y_end = area[1]
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                first_field_button[level][x][y].show()
                if second_field_button is not None:
                    second_field_button[level][x][y].show()

    @staticmethod
    def create_unchanged_labels(
            central_widget: QtWidgets.QWidget,
            data: Dict[str, List[int]], hide: bool) -> List[QtWidgets.QLabel]:
        labels: List[QtWidgets.QLabel] = []
        for inscription in data:
            x, y, width, height = data[inscription]
            label = QtWidgets.QLabel(central_widget)
            label.setText(inscription)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setWordWrap(True)
            if hide:
                label.hide()
            labels.append(label)
        return labels

    def create_inscriptions(
            self, central_widget: QtWidgets.QWidget,
            config_name: str, three_dimensional: bool) -> object:
        inscriptions_and_geometric_data \
            = self.config_parser.read_config_file(
              config_name)
        self.create_unchanged_labels(
            central_widget, inscriptions_and_geometric_data['general_labels'], hide=False)
        labels_first_lvl: List[QtWidgets.QLabel] = []
        labels_second_lvl: List[QtWidgets.QLabel] = []

        labels_first_lvl = self.create_unchanged_labels(
            central_widget, inscriptions_and_geometric_data['ships'], hide=False)
        if three_dimensional:
            labels_second_lvl = self.create_unchanged_labels(
                central_widget, inscriptions_and_geometric_data['submarine'], hide=True)
        return labels_first_lvl, labels_second_lvl

    def change_the_display_of_buttons(
            self, first_field_button, second_field_button,
            current_level: int, interval_x: Tuple[int, int],
            interval_y: Tuple[int, int]) -> None:
        self.hide_all_field_button(first_field_button, second_field_button)
        self.show_area_field_button(first_field_button, second_field_button,
                                    current_level, (interval_x, interval_y))

    @staticmethod
    def change_text_level_button(button_to_change_levels: QtWidgets.QPushButton) -> None:
        reverse_phrases = {
            'Перейти на нижний уровень': 'Перейти на верхний уровень',
            'Перейти на верхний уровень': 'Перейти на нижний уровень'
        }
        current_text = button_to_change_levels.text()
        new_text = reverse_phrases[current_text]
        button_to_change_levels.setText(new_text)

    @staticmethod
    def create_changed_labels(central_widget, data: Dict[str, List[int]],
                              hide: bool) -> Dict[str, QtWidgets.QLabel]:
        label_fields: Dict[str, QtWidgets.QLabel] = {}
        for ship in data:
            x, y, width, height = data[ship]
            ship_counter = QtWidgets.QLabel(central_widget)
            ship_counter.setGeometry(QtCore.QRect(x, y, width, height))
            ship_counter.setAlignment(QtCore.Qt.AlignCenter)
            ship_counter.setObjectName("ship")
            ship_counter.setText('0')
            if hide:
                ship_counter.hide()
            label_fields[ship] = ship_counter
        return label_fields

    def change_the_display_labels(
            self, label_fields_first_level: Dict[str, QtWidgets.QLabel],
            label_fields_second_level: Dict[str, QtWidgets.QLabel],
            labels_first_lvl: List[QtWidgets.QLabel],
            labels_second_lvl: List[QtWidgets.QLabel], result: bool) -> None:
        self.change_the_display_changed_labels(
            label_fields_second_level, show=result)
        self.change_the_display_changed_labels(
            label_fields_first_level, show=not result)

        self.change_the_display_unchanged_labels(
            labels_second_lvl, show=result)
        self.change_the_display_unchanged_labels(
            labels_first_lvl, show=not result)

    def create_label_fields(self, config_name: str, three_dimensional: bool, central_widget) \
            -> Tuple[Dict[str, QtWidgets.QLabel], Dict[str, QtWidgets.QLabel]]:
        data_for_fields = self.config_parser.read_config_file(config_name)
        label_fields_first_level: Dict[str, QtWidgets.QLabel] = {}
        label_fields_second_level: Dict[str, QtWidgets.QLabel] = {}

        label_fields_first_level = \
            self.create_changed_labels(central_widget, data_for_fields['ships'], hide=False)
        if three_dimensional:
            label_fields_second_level = \
                self.create_changed_labels(
                    central_widget, data_for_fields['submarine'], hide=True)
        return label_fields_first_level, label_fields_second_level

    def create_field_buttons(
            self, central_widget, field_size: Tuple[int, int], coordinate_grid: Tuple[List[int], List[int]],
            three_dimensional: bool, make_button_active: bool, method_for_connect_clicked) \
            -> Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]:
        style = self.config_parser.read_config_file('styles_for_element')
        field: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] \
            = {0: {}, 1: {}}
        x_coordinate_grid, y_coordinate_grid \
            = coordinate_grid
        for x in range(field_size[0]):
            field[0][x] = {}
            if three_dimensional:
                field[1][x] = {}
            for y in range(field_size[1]):
                button = QtWidgets.QPushButton(central_widget)
                button.setEnabled(make_button_active)
                x_coordinate, y_coordinate \
                    = x_coordinate_grid[x % 16], y_coordinate_grid[y % 16]
                button.setGeometry(x_coordinate, y_coordinate, 20, 20)
                button.setObjectName(f'button_field_{x}_{y}')
                button.setStyleSheet(style['button'])
                if make_button_active:
                    button.clicked.connect(
                        partial(method_for_connect_clicked, 0, (x, y)))
                field[0][x][y] = button
                if x > 15 or y > 15:
                    button.hide()
                if three_dimensional:
                    sublevel_button \
                        = QtWidgets.QPushButton(central_widget)
                    sublevel_button\
                        .setGeometry(x_coordinate, y_coordinate, 20, 20)
                    sublevel_button\
                        .setObjectName(f'sublevel_button_field_{x}_{y}')
                    sublevel_button.setEnabled(make_button_active)
                    sublevel_button.setStyleSheet(style['button'])
                    sublevel_button.hide()
                    if make_button_active:
                        sublevel_button.clicked.connect(
                            partial(method_for_connect_clicked, 1, (x, y)))
                    field[1][x][y] = sublevel_button
        return field

    @staticmethod
    def update_info_on_label(
            three_dimensional: bool, label_fields_first_level: Dict[str, QtWidgets.QLabel],
            label_fields_second_level: Dict[str, QtWidgets.QLabel], data_first_lvl: dict,
            data_second_lvl: dict) -> None:
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
            label_fields_first_level[translator_first_lvl[key]].setText(first_text)
            if three_dimensional:
                second_text = str(data_second_lvl[key])
                label_fields_second_level[translator_second_lvl[key]].setText(second_text)

    @staticmethod
    def calculate_window_size(field_size: Tuple[int, int], two_field: bool) -> Tuple[int, int]:
        width = 770 if two_field else 520
        if field_size[0] > 16:
            return width, 770
        elif field_size[0] == 16:
            return width, 560
        else:
            return 520, 400
