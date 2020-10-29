from logic.arrange_the_ships_logic import ArrangeTheShipsLogic
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


if __name__ == '__main__':
    pass
