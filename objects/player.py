from typing import Tuple

from work_with_confg.config_handler import ConfigHandler


class Player:
    def __init__(self, ships: []):
        self.field = ships
        config_parser = ConfigHandler()
        self.hits_statuses = config_parser.read_config_file('hits_statuses')

    def process_a_shot(self, level: int, point: (int, int)):
        check, index_ship = self.is_a_ship(level, point)
        if check:
            ship = self.field[index_ship]
            ship.size -= 1
            if ship.size == 0:
                ship.alive = False
                return self.hits_statuses['kill'], ship.position
            return self.hits_statuses['wound'], None
        return self.hits_statuses['fluffed'], None

    def is_a_ship(self, level: int, point: (int, int)) -> Tuple[bool, int]:
        for index, ship in enumerate(self.field):
            if ship.level == level:
                if point in ship.position:
                    return True, index
        return False, None

    def live_ships_remained(self) -> bool:
        for ship in self.field:
            if ship.alive:
                return True
        return False
