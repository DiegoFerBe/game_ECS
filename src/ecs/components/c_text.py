

import pygame


class CText:
    def __init__(self, text: str,color:pygame.Color,font:pygame.font.Font):
        self.text = text
        self.color = color
        self.font = font
