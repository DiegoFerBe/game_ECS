from typing import Dict, List
import pygame

class CEnemySpawner:
    def __init__(self, spawn_events: List[Dict]) -> None:
        self.spawn_events = spawn_events
        self.timer = 0.0  
        self.current_index = 0