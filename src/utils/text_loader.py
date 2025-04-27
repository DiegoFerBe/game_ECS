

import esper
import pygame

from src.create.prefab_rectangle import create_text
from src.ecs.components.tags.c_tag_ui import UIType


def load_text(world:esper.World,text_config:dict):

    for key, text_data in text_config.items():
        text = text_data['text']
        position = pygame.Vector2(text_data['position']["x"], text_data['position']["y"])
        color = pygame.color.Color(text_data['color']['r'], text_data['color']['g'], text_data['color']['b'])
        ui_type = UIType[text_data['type']]  # Convierte "GAMEPLAY", "PAUSE", etc., al enum correspondiente

        create_text(world,text,position,color,ui_type)

    