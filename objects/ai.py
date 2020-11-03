from logic.arrange_the_ships_logic import ArrangeTheShipsLogic
from random import randint

from logic.field import Field


class AI:
    def __init__(self, field_size: [int], three_dimensional: bool):
        self.field_size = field_size
        self.three_dimensional = three_dimensional
        self.field = self.place_ships()
        self.where_did_i_shoot = []

    def place_ships(self) -> list:
        handler = ArrangeTheShipsLogic(
            self.field_size, self.three_dimensional, for_test=True)
        number_of_cells = self.field_size[0] * self.field_size[1]
        number_of_ships = handler.calculate_the_number_of_related_entity_on_the_field(number_of_cells)
        handler.field_for_related_entity = handler.create_start_field_for_related_entity()
        handler.fill_stack_related_entity(number_of_ships)
        while len(handler.stack_related_entity_first_lvl) > 0:
            level = 0
            if self.three_dimensional:
                level = randint(0, 1)
            x = randint(0, self.field_size[0] - 1)
            y = randint(0, self.field_size[1] - 1)
            handler.processing_options_for_the_location_of_the_ship(level, (x, y))
        information_about_all_related_entity \
            = handler.get_information_about_all_related_entity()
        field = Field(information_about_all_related_entity)
        return field.ships

    def process_a_shot(self, level: int, point: (int, int)):
        check, index_ship = self.is_a_ship(level, point)
        if check:
            ship = self.field[index_ship]
            ship.size -= 1
            if ship.size == 0:
                ship.alive = False
                return 'kill', ship.position
            return 'wound', None
        return 'fluffed', None

    def is_a_ship(self, level: int, point: (int, int)) -> (bool, int):
        for index, ship in enumerate(self.field):
            if ship.level == level:
                if point in ship.position:
                    return True, index
        return False, None

    def update_used_cells(self, ship):
        start_x = max(0, ship[0][0] - 1)
        start_y = max(0, ship[0][1] - 1)
        end_x = min(self.field_size[0] - 1, ship[-1][0] + 1)
        end_y = min(self.field_size[1] - 1, ship[-1][1] + 1)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if (x, y) not in self.where_did_i_shoot:
                    self.where_did_i_shoot.append((x, y))

    def do_shoot(self):
        level = 0
        if self.three_dimensional:
            level = randint(0, 1)
        x = randint(0, self.field_size[0] - 1)
        y = randint(0, self.field_size[1] - 1)
        if (level, x, y) not in self.where_did_i_shoot:
            self.where_did_i_shoot.append((x, y))
            return level, (x, y)

    def live_ships_remained(self) -> bool:
        for ship in self.field:
            if ship.alive:
                return True
        return False
