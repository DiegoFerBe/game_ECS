import pygame

class CTransform:
    def __init__(self, position: pygame.Vector2) -> None:
        self.position = position
        self.spawn_position = position.copy()
