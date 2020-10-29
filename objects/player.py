class Player:
    def __init__(self, ships: []):
        self.field = ships

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

    def live_ships_remained(self) -> bool:
        for ship in self.field:
            if ship.alive:
                return True
        return False
