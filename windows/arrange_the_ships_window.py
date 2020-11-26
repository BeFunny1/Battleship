import sys
from functools import partial
from typing import Dict, List, Tuple

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow

from windows.window_create_helper import WindowCreateHelper
from work_with_confg.config_handler import ConfigHandler


class ArrangeTheShipsWindow(QMainWindow):
    def __init__(self, field_size: (int, int), three_dimensional: bool) -> None:
        super().__init__()
        self.config_parser = ConfigHandler()
        self.window_create_helper = WindowCreateHelper()
        self.field_size = field_size
        self.three_dimensional = three_dimensional

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.current_level: int = 0
        self.interval_x: Tuple[int, int] \
            = (0, 15) if self.field_size[0] >= 15 else (0, 9)
        self.interval_y: Tuple[int, int] \
            = (0, 15) if self.field_size[1] >= 15 else (0, 9)

        self.labels_first_lvl: List[QtWidgets.QLabel] = None
        self.labels_second_lvl: List[QtWidgets.QLabel] = None

        self.button_del_activity: bool = False

        self.labels_for_display_interval: Dict[str, QtWidgets.QLabel] = None
        self.field_button: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] = None
        self.label_fields_first_level: Dict[str, QtWidgets.QLabel] = None
        self.label_fields_second_level: Dict[str, QtWidgets.QLabel] = None
        self.activate_delete_label: QtWidgets.QLabel = None
        self.start_game_button: QtWidgets.QPushButton = None

        self.customer = None
        self.exit_the_window = None

    def establish_communication(self, customer, exit_the_window) -> None:
        self.customer = customer
        self.exit_the_window = exit_the_window

    def setupUi(self) -> None:
        self.customize_window()
        self.labels_first_lvl, self.labels_second_lvl \
            = self.create_inscriptions()
        self.label_fields_first_level, \
            self.label_fields_second_level, \
            self.activate_delete_label \
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

    def create_direction_arrows_button(self) \
            -> Dict[str, QtWidgets.QPushButton]:
        arrows_button: Dict[str, QtWidgets.QPushButton] = \
            self.window_create_helper.create_direction_arrows_button(
                window='arrange', central_widget=self.central_widget,
                method_for_make_a_shift_in_the_field=self.make_a_shift_in_the_field)
        return arrows_button

    def make_a_shift_in_the_field(self, direction: str) -> None:
        self.interval_x, self.interval_y, shift_occurred \
            = self.window_create_helper.make_a_shift_in_the_interval(
              direction, self.interval_x, self.interval_y, self.field_size)
        if shift_occurred:
            self.hide_all_field_button()
            self.show_area_field_button(
                self.current_level, area=(self.interval_x, self.interval_y))
            self.update_labels_with_intervals()

    def create_labels_with_intervals(self) -> Dict[str, QtWidgets.QLabel]:
        labels: Dict[str, QtWidgets.QLabel] \
            = self.window_create_helper.create_labels_with_intervals(
            self.central_widget, config_file='label_field_arrange_the_ships_window')
        return labels

    def update_labels_with_intervals(self) -> None:
        self.window_create_helper.update_labels_with_intervals(
            config_name='label_field_arrange_the_ships_window', interval_x=self.interval_x,
            interval_y=self.interval_y, labels_for_display_interval=self.labels_for_display_interval)

    def hide_all_field_button(self) -> None:
        self.window_create_helper.hide_all_field_button(
            first_field_button=self.field_button, second_field_button=None)

    def show_area_field_button(
            self, level: int, area: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        self.window_create_helper.show_area_field_button(
            first_field_button=self.field_button,
            second_field_button=None,
            level=level, area=area)

    def update_info_on_label(
            self, data_first_lvl: dict, data_second_lvl: dict) -> None:
        self.window_create_helper.update_info_on_label(
            three_dimensional=self.three_dimensional,
            label_fields_first_level=self.label_fields_first_level,
            label_fields_second_level=self.label_fields_second_level,
            data_first_lvl=data_first_lvl,
            data_second_lvl=data_second_lvl)

    def create_button_to_change_levels(self) -> QtWidgets.QPushButton:
        geometric_data: Tuple[int, int, int, int] = (220, 90, 260, 30)
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

    def change_the_display_labels(self, result: bool) -> None:
        self.window_create_helper.change_the_display_labels(
            label_fields_first_level=self.label_fields_first_level,
            label_fields_second_level=self.label_fields_second_level,
            labels_first_lvl=self.labels_first_lvl,
            labels_second_lvl=self.labels_second_lvl, result=result)

    def change_the_display_of_buttons(self) -> None:
        self.window_create_helper.change_the_display_of_buttons(
            first_field_button=self.field_button, second_field_button=None,
            current_level=self.current_level, interval_x=self.interval_x, interval_y=self.interval_y)

    def change_the_display_unchanged_labels(
            self, data: List[QtWidgets.QLabel], show: bool) -> None:
        self.window_create_helper.change_the_display_unchanged_labels(data, show)

    def change_the_display_changed_labels(
            self, data: Dict[str, QtWidgets.QLabel], show: bool) -> None:
        self.window_create_helper.change_the_display_changed_labels(data, show)

    def create_field_buttons(self) \
            -> Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]]:
        coordinate_grid = self.get_coordinate_grid()
        field: Dict[int, Dict[int, Dict[int, QtWidgets.QPushButton]]] \
            = self.window_create_helper.create_field_buttons(
              central_widget=self.central_widget, field_size=self.field_size,
              coordinate_grid=coordinate_grid, three_dimensional=self.three_dimensional,
              make_button_active=True, method_for_connect_clicked=self.customer)
        return field

    def get_coordinate_grid(self) -> Tuple[List[int], List[int]]:
        x_coordinates = []
        y_coordinates = []
        if self.field_size[0] > 15:
            x_start = 100
            y_start = 150
        else:
            x_start = self.width() // 2 - (self.field_size[0] // 2 * 20)
            y_start = 130
        for i in range(16):
            x_coordinates.append(x_start + i * 20)
            y_coordinates.append(y_start + i * 20)
        return x_coordinates, y_coordinates

    def switch_start_game_button(self, toggle: bool) -> None:
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

    def update_buttons_text(
            self, level: int, x: int, y: int, text: str) -> None:
        if text == '':
            self.field_button[level][x][y].setIcon(QtGui.QIcon('./images/white_background.jpg'))
        else:
            self.field_button[level][x][y].setIcon(QtGui.QIcon('./images/ship.jpg'))

    def del_button_event(self) -> None:
        reverse_phrases = {
            'активирован': 'деактивирован',
            'деактивирован': 'активирован'
        }
        current_text = self.activate_delete_label.text()
        new_text = reverse_phrases[current_text]
        self.activate_delete_label.setText(new_text)
        self.button_del_activity = not self.button_del_activity

    def create_label_fields(self) \
            -> Tuple[Dict[str, QtWidgets.QLabel], Dict[str, QtWidgets.QLabel], QtWidgets.QLabel]:
        label_fields_first_level, label_fields_second_level \
            = self.window_create_helper.create_label_fields(
              config_name='label_field_arrange_the_ships_window',
              three_dimensional=self.three_dimensional,
              central_widget=self.central_widget)
        activate_delete_label = self.create_activate_del_label()
        return label_fields_first_level, label_fields_second_level, activate_delete_label

    def create_activate_del_label(self) -> QtWidgets.QLabel:
        data_for_label: Tuple[int, int, int, int] \
            = self.config_parser.read_config_file('label_field_arrange_the_ships_window')['sub_level_activate']
        x, y, width, height = data_for_label
        activate_delete_label = QtWidgets.QLabel(self.central_widget)
        activate_delete_label.setGeometry(QtCore.QRect(x, y, width, height))
        activate_delete_label.setAlignment(QtCore.Qt.AlignCenter)
        activate_delete_label.setObjectName("ship")
        activate_delete_label.setText('деактивирован')
        return activate_delete_label

    def create_inscriptions(self) \
            -> Tuple[List[QtWidgets.QLabel], List[QtWidgets.QLabel]]:
        labels_first_lvl: List[QtWidgets.QLabel] = []
        labels_second_lvl: List[QtWidgets.QLabel] = []
        labels_first_lvl, labels_second_lvl \
            = self.window_create_helper.create_inscriptions(
              self.central_widget,
              three_dimensional=self.three_dimensional,
              config_name='inscriptions_and_geometric_data_arrange_the_ships_window')
        return labels_first_lvl, labels_second_lvl

    def create_unchanged_labels(
            self, data: Dict[str, List[int]], hide: bool) -> List[QtWidgets.QLabel]:
        labels: List[QtWidgets.QLabel] \
            = self.window_create_helper.create_unchanged_labels(
              self.central_widget, data, hide=hide)
        return labels

    def customize_window(self) -> None:
        window_size = self.calculate_window_size()
        self.window_create_helper.customize_window(self, 'Расставление кораблей', window_size)

    def calculate_window_size(self) -> Tuple[int, int]:
        width, height = self.window_create_helper.calculate_window_size(
            self.field_size, two_field=False)
        return width, height


if __name__ == '__main__':
    application_for_window = QtWidgets.QApplication(sys.argv)
    app = ArrangeTheShipsWindow((10, 10), False)
    app.create_config_window()
    application_for_window.exec_()
