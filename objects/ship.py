from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Ship:
    level: int
    size: int
    position: List[Tuple[int, int]]
    alive: bool
