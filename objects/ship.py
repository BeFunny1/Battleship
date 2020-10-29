from copy import copy


class Ship:
    def __init__(self, level: int, size: int, position: [], alive: True):
        self.level = level
        self.size = size
        self.position = copy(position)
        self.alive = alive
