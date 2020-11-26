from typing import List, Tuple

from objects.ship import Ship


class Field:
    def __init__(self, related_entity: List[Tuple[int, List[Tuple[int, int]]]]):
        self.ships = self.parse_related_entity_to_the_ships(related_entity)

    @staticmethod
    def parse_related_entity_to_the_ships(
            related_entity: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Ship]:
        ships = []
        for element in related_entity:
            level = element[0]
            position = element[1]
            size = len(position)
            ship = Ship(level, size, position, alive=True)
            ships.append(ship)
        return ships
