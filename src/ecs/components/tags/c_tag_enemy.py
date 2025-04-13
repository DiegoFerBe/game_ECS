
from enum import Enum


class CEnemyType(Enum):
    STANDARD = 0
    HUNTER = 1

class CTagEnemy:
    def __init__(self, type: CEnemyType= CEnemyType.STANDARD) -> None:
        self.type = type