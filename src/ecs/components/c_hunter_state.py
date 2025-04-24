from enum import Enum


class CHunterState:
    def __init__(self):
        self.state = HunterState.IDLE
        self.sound_played = False 


class HunterState(Enum):
    IDLE = 0
    MOVE = 1
    RETURN = 2