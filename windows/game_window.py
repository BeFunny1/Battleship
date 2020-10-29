from functools import partial

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

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

    def setupUi(self) -> None:
        self.customize_window()
        self.player_buttons = self.create_field_buttons_player()
        self.enemy_buttons = self.create_field_buttons_enemy()

        # self.create_inscriptions()
        # self.labels_field = self.create_label_fields()

        if self.three_dimensional:
            self.button_to_change_level = self.create_button_to_change_levels()

    def display_all_player_ship(self, ships: []):
        for ship in ships:
            level = ship.level
            text = str(ship.size)
            for position in ship.position:
                x = position[0]
                y = position[1]
                self.player_buttons[level][x][y].setText(text)

    def create_label_fields(self) -> {QtWidgets.QLabel}:
        data_for_fields = self.config_reader.read_config_file(
                          'label_field_game_window')
        label_fields = {}
        for ship in data_for_fields.keys():
            x, y, width, height = data_for_fields[ship]
            ship_counter = QtWidgets.QLabel(self.central_widget)
            ship_counter.setGeometry(QtCore.QRect(x, y, width, height))
            ship_counter.setAlignment(QtCore.Qt.AlignCenter)
            ship_counter.setObjectName("ship")
            ship_counter.setText('0')
            label_fields[ship] = ship_counter
        return label_fields

    def create_inscriptions(self) -> None:
        inscriptions_and_geometric_data \
            = self.config_reader.read_config_file(
              'inscriptions_and_geometric_data_game_window')
        for inscription in inscriptions_and_geometric_data:
            x, y, width, height = inscriptions_and_geometric_data[inscription]
            label = QtWidgets.QLabel(self.central_widget)
            label.setText(inscription)
            label.setGeometry(QtCore.QRect(x, y, width, height))
            label.setObjectName("label")
            label.setWordWrap(True)

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
        result = self.player_buttons[1][0][0].isHidden()

        self.change_the_display_of_buttons(self.player_buttons[1], show=result)
        self.change_the_display_of_buttons(self.player_buttons[0], show=not result)

        self.change_the_display_of_buttons(self.enemy_buttons[1], show=result)
        self.change_the_display_of_buttons(self.enemy_buttons[0], show=not result)

    @staticmethod
    def change_the_display_of_buttons(field: dict, show: bool) -> None:
        for x in field.keys():
            for y in field[x].keys():
                if show:
                    field[x][y].show()
                else:
                    field[x][y].hide()

    def create_field_buttons_player(self) -> {}:
        start_x_player = 40
        buttons = self.create_field_buttons(start_x_player, is_a_player=True)
        return buttons

    def create_field_buttons_enemy(self) -> {}:
        start_x_enemy = 40 + 20 * self.one_field_size[0] + 50
        buttons = self.create_field_buttons(start_x_enemy, is_a_player=False)
        return buttons

    def establish_connection(self, player_shot_handler):
        self.player_shot_handler = player_shot_handler

    def create_field_buttons(self, start_x: int, is_a_player: bool) -> {}:
        field = {0: {}, 1: {}}
        start_y = 130
        for x in range(self.one_field_size[0]):
            field[0][x] = {}
            if self.three_dimensional:
                field[1][x] = {}
            for y in range(self.one_field_size[1]):
                button = QtWidgets.QPushButton(self.central_widget)
                button.setEnabled(not is_a_player)
                button.setGeometry(QtCore.QRect(
                    start_x + 20 * x, start_y + 20 * y, 20, 20))
                button.setObjectName(
                    f'button_main_field_{str(x)}_{str(y)}')

                if not is_a_player:
                    button.clicked.connect(
                        partial(self.player_shot_handler, 0, (x, y)))
                field[0][x][y] = button
                if self.three_dimensional:
                    sublevel_button = QtWidgets.QPushButton(self.central_widget)
                    sublevel_button.setEnabled(not is_a_player)
                    sublevel_button.setGeometry(QtCore.QRect(
                        start_x + 20 * x, start_y + 20 * y, 20, 20))
                    sublevel_button.setObjectName(
                        f'button_sublevel_field_{str(x)}_{str(y)}')

                    if not is_a_player:
                        button.clicked.connect(
                            partial(self.player_shot_handler, 0, (x, y)))
                    sublevel_button.hide()
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
        window_weight, window_height = self.calculate_window_size()
        self.setObjectName('MainWindow')
        self.setWindowTitle('Игра')
        self.resize(window_weight, window_height)
        self.setMinimumSize(QtCore.QSize(window_weight, window_height))
        self.setMaximumSize(QtCore.QSize(window_weight, window_height))

    def calculate_window_size(self) -> (int, int):
        window_weight = max(520, 40 + 20 * self.one_field_size[0]
                            + 50 + 20 * self.one_field_size[0] + 40)
        window_height = 90 + 10 + 20 * self.one_field_size[1] + 100
        return window_weight, window_height
