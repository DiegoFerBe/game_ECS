
from enum import Enum


class UIType(Enum):
    GAMEPLAY = 0
    MENU=1
    HUD=2
    PAUSE=3



class CTagUI:
    def __init__(self, type: UIType = UIType.GAMEPLAY) -> None:
        self.type = type