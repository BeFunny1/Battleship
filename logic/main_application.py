from typing import Dict, Tuple, List

from logic.arrange_the_ships_logic import ArrangeTheShipsLogic
from logic.field import Field
from logic.game_logic import Game
from objects.ship import Ship
from windows.configuration_window import ConfigurationWindow


class Application:
    def __init__(self):
        self.config_window: ConfigurationWindow = None
        self.arrange_the_ships: ArrangeTheShipsLogic = None
        self.game: Game = None

        self.field_size: Tuple[int, int] = None
        self.ai_level: str = None
        self.three_dimensional_map: bool = None

    def create_config_window(self) -> None:
        self.config_window = ConfigurationWindow()
        self.config_window.setupUi()
        self.config_window.show()
        self.config_window.establish_communication(
            self.create_arrange_the_ships_window)

    def create_arrange_the_ships_window(
            self, permission, three_dimensional_map, ai_level) -> None:
        self.three_dimensional_map = three_dimensional_map
        self.ai_level = ai_level

        self.config_window.hide()
        self.field_size = tuple(map(int, permission.split('x')))

        # self.go_to_the_game(None, None)
        self.arrange_the_ships \
            = ArrangeTheShipsLogic(
              self.field_size, self.three_dimensional_map, for_test=False)
        self.arrange_the_ships.establish_communication(
            self.go_to_the_game)

    def go_to_the_game(
            self, information: list, number_of_ships_per_level: Dict[int, int]) -> None:
        self.arrange_the_ships.hide_window()
        field = Field(information)

        # ships, number_of_ships = self.create_player_ships_automatic()

        self.game = Game(self.field_size,
                         self.three_dimensional_map,
                         field.ships, number_of_ships_per_level,
                         # ships, number_of_ships,
                         self.ai_level)

    def create_player_ships_automatic(self) -> Tuple[List[Ship], Dict[int, int]]:
        from objects.ai import AI
        test = AI(self.field_size, self.three_dimensional_map, 'easy')
        number_of_cells = self.field_size[0] * self.field_size[1]
        self.arrange_the_ships \
            = ArrangeTheShipsLogic(
                self.field_size, self.three_dimensional_map, for_test=True)
        number_of_ships \
            = self.arrange_the_ships.calculate_the_number_of_related_entity_on_the_field(
                number_of_cells)
        return test.ships, number_of_ships


if __name__ == '__main__':
    pass
