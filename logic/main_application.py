from logic.arrange_the_ships_logic import ArrangeTheShipsLogic
from logic.field import Field
from windows.configuration_window import ConfigurationWindow


class Application:
    def __init__(self):
        self.config_window = None
        self.arrange_the_ships = None

    def create_config_window(self):
        self.config_window = ConfigurationWindow()
        self.config_window.setupUi()
        self.config_window.show()
        self.config_window.establish_communication(self.create_arrange_the_ships_window)

    def create_arrange_the_ships_window(self, permission, three_dimensional_map, ai_level):
        self.config_window.hide()
        field_size = list(map(int, permission.split('x')))

        self.arrange_the_ships \
            = ArrangeTheShipsLogic(
              field_size, three_dimensional_map, for_test=False)
        self.arrange_the_ships.establish_communication(self.go_to_the_game)

    def go_to_the_game(self, information: list):
        self.arrange_the_ships.hide_window()
        field = Field()
        ships = field.parse_related_entity_to_the_ships(information)
        print(information)


if __name__ == '__main__':
    pass
