import pygame

class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> 'CSurface':
        instance = cls(surface.get_size(), pygame.Color(0, 0, 0))
        instance.surface = surface
        instance.area = surface.get_rect()
        return instance
    
    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: pygame.Color) -> 'CSurface':
        text_surface = font.render(text, True, color)
        instance = cls(text_surface.get_size(), pygame.Color(0, 0, 0))
        instance.surface = text_surface
        instance.area = text_surface.get_rect()
        return instance