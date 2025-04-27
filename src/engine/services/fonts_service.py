
import pygame


class FontsService:
    def __init__(self):
        self.fonts = {}

    def get_font(self, font_path:str) -> pygame.font.Font: 
        if font_path not in self.fonts:
            self.fonts[font_path] = pygame.font.Font(font_path, 12)
        return self.fonts[font_path]