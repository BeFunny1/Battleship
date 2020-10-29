from objects.ship import Ship


class Field:
    @staticmethod
    def parse_related_entity_to_the_ships(related_entity: list) -> list:
        ships = []
        for element in related_entity:
            level = element[0]
            position = element[1]
            size = len(position)
            ship = Ship(level, size, position, alive=True)
            ships.append(ship)
        return ships
