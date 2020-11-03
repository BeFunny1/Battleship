from logic.arrange_the_ships_logic import ArrangeTheShipsLogic
from logic.field import Field
from logic.game_logic import Game
from windows.configuration_window import ConfigurationWindow


class Application:
    def __init__(self):
        self.config_window = None
        self.arrange_the_ships = None
        self.game = None

        self.field_size = None
        self.ai_level = None
        self.three_dimensional_map = None

    def create_config_window(self):
        self.config_window = ConfigurationWindow()
        self.config_window.setupUi()
        self.config_window.show()
        self.config_window.establish_communication(self.create_arrange_the_ships_window)

    def create_arrange_the_ships_window(self, permission, three_dimensional_map, ai_level):
        self.three_dimensional_map = three_dimensional_map
        self.ai_level = self.ai_level

        self.config_window.hide()
        self.field_size = list(map(int, permission.split('x')))

        self.arrange_the_ships \
            = ArrangeTheShipsLogic(
              self.field_size, self.three_dimensional_map, for_test=False)
        self.arrange_the_ships.establish_communication(self.go_to_the_game)

    def go_to_the_game(self, information: list):
        self.arrange_the_ships.hide_window()
        field = Field(information)
        self.game = Game(self.field_size, self.three_dimensional_map, field.ships)


if __name__ == '__main__':
    pass
