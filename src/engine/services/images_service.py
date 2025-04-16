import pygame

class ImagesService:
    def __init__(self):
       self.images = {}

    def get(self, path: str) -> pygame.Surface:
        if path not in self.images:
            self.images[path] = pygame.image.load(path).convert_alpha()
        return self.images[path]