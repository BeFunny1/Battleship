import sys
from functools import partial
from typing import Dict, List, Tuple

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow

from work_with_confg.config_handler import ConfigHandler


class ArrangeTheShipsWindow(QMainWindow):
    def __init__(self, field_size: (int, int), three_dimensional: bool):
        super().__init__()
        self.config_reader = ConfigHandler()
        self.field_size = field_size
        self.three_dimensional = three_dimensional

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.current_level: int = 0
        self.interval_x: Tuple[int, int] = (0, 15)
        self.interval_y: Tuple[int, int] = (0, 15)

        self.labels_first_lvl = None
        self.labels_second_lvl = None

        self.button_del_activity = False
        self.labels_for_display_interval = None
        self.field_button = None
        self.label_fields_first_level = None
        self.label_fields_second_level = None
        self.activate_delete_label = None
        self.start_game_button = None

        self.customer = None
        self.exit_the_window = None

    def establish_communication(self, customer, exit_the_window):
        self.customer = customer
        self.exit_the_window = exit_the_window

    def setupUi(self) -> None:
        self.customize_window()
        self.labels_first_lvl, self.labels_second_lvl \
            = self.create_inscriptions()
        self.label_fields_first_level, self.label_fields_second_level, self.activate_delete_label \
            = self.create_label_fields()
        self.create_del_button()
        self.start_game_button \
            = self.create_start_game_button()

        if self.three_dimensional:
            self.create_button_to_change_levels()
        if self.field_size[0] > 16:
            self.create_direction_arrows_button()
            self.labels_for_display_interval \
                = self.create_labels_with_intervals()
            self.update_labels_with_intervals()
        self.field_button = self.create_field_buttons()

    def create_direction_arrows_button(self) -> Dict[str, QtWidgets.QPushButton]:
        data_for_buttons = self.config_reader.read_config_file(
            'direction_arrows_button')
        arrows_button: Dict[str, QtWidgets.QPushButton] = {}
        for direction in data_for_buttons.keys():
            text, geometric_data = list(data_for_buttons[direction].items())[0]
            x, y, width, height = geometric_data['arrange']
            button = QtWidgets.QPushButton(self.central_widget)
            button.setGeometry(QtCore.QRect(x, y, width, height))
            button.setObjectName(f'arrows_button_{direction}')
            button.setText(text)
            button.clicked.connect(partial(self.make_a_shift_in_the_field, direction))
            arrows_button[direction] = button
        return arrows_button

    def make_a_shift_in_the_field(self, direction: str) -> None:
        if direction == 'right' and self.interval_x[1] < self.field_size[0] - 1:
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
        elif direction == 'down' and self.interval_y[1] < self.field_size[1] - 1:
            self.hide_all_field_button()
            self.interval_y = self.interval_y[0] + 16, self.interval_y[1] + 16
            self.show_area_field_button(self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

    def create_labels_with_intervals(self):
        data = self.config_reader.read_config_file(
            'label_field_arrange_the_ships_window')
        data_for_labels = data['interval']
        labels: Dict[str, QtWidgets.QLabel] = {}
        for key in data_for_labels.keys():
            x, y, width, height = data_for_labels[key]
            label = QtWidgets.QLabel(self.central_widget)
            label.setText(key)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setAlignment(QtCore.Qt.AlignRight)
            if key == 'x_start':
                label.setAlignment(QtCore.Qt.AlignLeft)
            labels[key] = label
        return labels

    def update_labels_with_intervals(self):
        self.labels_for_display_interval['x_start'].setText(str(self.interval_x[0]))
        self.labels_for_display_interval['x_end'].setText(str(self.interval_x[1]))
        self.labels_for_display_interval['y_start'].setText(str(self.interval_y[0]))
        self.labels_for_display_interval['y_end'].setText(str(self.interval_y[1]))

    def hide_all_field_button(self) -> None:
        for level in self.field_button.keys():
            for x in self.field_button[level]:
                for y in self.field_button[level][x]:
                    self.field_button[level][x][y].hide()

    def show_area_field_button(self, level: int, area: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        x_start, x_end = area[0]
        y_start, y_end = area[1]
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.field_button[level][x][y].show()

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
            self.label_fields_first_level[translator_first_lvl[key]].setText(str(data_first_lvl[key]))
            if self.three_dimensional:
                self.label_fields_second_level[translator_second_lvl[key]].setText(str(data_second_lvl[key]))

    def create_button_to_change_levels(self) -> QtWidgets.QPushButton:
        button_to_change_levels = QtWidgets.QPushButton(self.central_widget)
        button_to_change_levels.setGeometry(QtCore.QRect(220, 90, 261, 28))
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
        result = self.current_level == 0
        if result:
            self.current_level = 1
        else:
            self.current_level = 0

        self.change_the_display_of_buttons()

        self.change_the_display_changed_labels(self.label_fields_second_level, show=result)
        self.change_the_display_changed_labels(self.label_fields_first_level, show=not result)

        self.change_the_display_unchanged_labels(self.labels_second_lvl, show=result)
        self.change_the_display_unchanged_labels(self.labels_first_lvl, show=not result)

    def change_the_display_of_buttons(self) -> None:
        self.hide_all_field_button()
        self.show_area_field_button(self.current_level,
                                    (self.interval_x, self.interval_y))

    @staticmethod
    def change_the_display_unchanged_labels(data: List[QtWidgets.QLabel], show: bool) -> None:
        for label in data:
            if show:
                label.show()
            else:
                label.hide()

    @staticmethod
    def change_the_display_changed_labels(data: Dict[str, QtWidgets.QLabel], show: bool) -> None:
        for label in data.keys():
            if show:
                data[label].show()
            else:
                data[label].hide()

    def create_field_buttons(self) -> Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]:
        style = self.config_reader.read_config_file('styles_for_element')
        field: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] = {0: {}, 1: {}}
        x_coordinate_grid, y_coordinate_grid = self.get_coordinate_grid()
        for x in range(self.field_size[0]):
            field[0][x] = {}
            if self.three_dimensional:
                field[1][x] = {}
            for y in range(self.field_size[1]):
                button = QtWidgets.QPushButton(self.central_widget)
                x_coordinate, y_coordinate = x_coordinate_grid[x % 16], y_coordinate_grid[y % 16]
                button.setGeometry(x_coordinate, y_coordinate, 20, 20)
                button.setObjectName(f'button_field_{x}_{y}')
                button.clicked.connect(
                    partial(self.customer, 0, (x, y)))
                button.setStyleSheet(style['button'])
                field[0][x][y] = button
                if x > 15 or y > 15:
                    button.hide()
                if self.three_dimensional:
                    sublevel_button = QtWidgets.QPushButton(self.central_widget)
                    sublevel_button.setGeometry(x_coordinate, y_coordinate, 20, 20)
                    sublevel_button.setObjectName(f'sublevel_button_field_{x}_{y}')
                    sublevel_button.setStyleSheet(style['button'])
                    sublevel_button.hide()
                    sublevel_button.clicked.connect(
                        partial(self.customer, 1, (x, y)))
                    field[1][x][y] = sublevel_button
        return field

    def get_coordinate_grid(self) -> Tuple[List[int], List[int]]:
        x_coordinates = []
        y_coordinates = []
        if self.field_size[0] > 15:
            x_start = 100
            y_start = 150
        else:
            x_start = self.width() // 2 - (self.field_size[0] // 2 * 20)
            y_start = 120
        for i in range(16):
            x_coordinates.append(x_start + i * 20)
            y_coordinates.append(y_start + i * 20)
        return x_coordinates, y_coordinates

    def switch_start_game_button(self, toggle: bool):
        self.start_game_button.setEnabled(toggle)

    def create_start_game_button(self) -> QtWidgets.QPushButton:
        start_game_button = QtWidgets.QPushButton(self.central_widget)
        x = self.width() // 2 - 140
        y = self.height() - 60
        start_game_button.setGeometry(QtCore.QRect(x, y, 280, 30))
        start_game_button.setObjectName("start_game_button")
        start_game_button.setText('Начать игру')
        start_game_button.setEnabled(False)
        start_game_button.clicked.connect(self.exit_the_window)
        return start_game_button

    def create_del_button(self) -> QtWidgets.QPushButton:
        del_button = QtWidgets.QPushButton(self.central_widget)
        del_button.setGeometry(QtCore.QRect(410, 20, 81, 51))
        del_button.setObjectName("del_button")
        del_button.setText('DEL')
        del_button.clicked.connect(self.del_button_event)
        return del_button

    def update_buttons_text(self, level: int, x: int, y: int, text: str) -> None:
        self.field_button[level][x][y].setText(text)

    def del_button_event(self) -> None:
        reverse_phrases = {
            'активирован': 'деактивирован',
            'деактивирован': 'активирован'
        }
        current_text = self.activate_delete_label.text()
        new_text = reverse_phrases[current_text]
        self.activate_delete_label.setText(new_text)
        self.button_del_activity = not self.button_del_activity

    def create_label_fields(self) -> Tuple[Dict[str, QtWidgets.QLabel], Dict[str, QtWidgets.QLabel], QtWidgets.QLabel]:
        data_for_fields = self.config_reader.read_config_file(
                          'label_field_arrange_the_ships_window')
        label_fields_first_level: Dict[str, QtWidgets.QLabel] = {}
        label_fields_second_level: Dict[str, QtWidgets.QLabel] = {}

        label_fields_first_level = \
            self.create_changed_labels(data_for_fields['ships'], hide=False)
        if self.three_dimensional:
            label_fields_second_level = \
                self.create_changed_labels(data_for_fields['submarine'], hide=True)
        activate_delete_label = QtWidgets.QLabel(self.central_widget)
        x, y, width, height = data_for_fields['sub_level_activate']
        activate_delete_label.setGeometry(QtCore.QRect(x, y, width, height))
        activate_delete_label.setAlignment(QtCore.Qt.AlignCenter)
        activate_delete_label.setObjectName("ship")
        activate_delete_label.setText('деактивирован')
        return label_fields_first_level, label_fields_second_level, activate_delete_label

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
              'inscriptions_and_geometric_data_arrange_the_ships_window')
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

    def customize_window(self):
        window_weight, window_height = self.calculate_window_size()
        self.setObjectName('MainWindow')
        self.setWindowTitle('Заполнение поля')
        self.resize(window_weight, window_height)
        self.setMinimumSize(QtCore.QSize(window_weight, window_height))
        self.setMaximumSize(QtCore.QSize(window_weight, window_height))

    def calculate_window_size(self) -> (int, int):
        if self.field_size[0] > 16:
            return 520, 770
        elif self.field_size[0] == 16:
            return 520, 560
        else:
            return 520, 400
        # window_weight = max(520, 40 + 20 * self.field_size[0] + 40)
        # window_height = 90 + 10 + 20 * self.field_size[1] + 100
        # return window_weight, window_height


if __name__ == '__main__':
    application_for_window = QtWidgets.QApplication(sys.argv)
    app = ArrangeTheShipsWindow((10, 10), False)
    app.create_config_window()
    application_for_window.exec_()
