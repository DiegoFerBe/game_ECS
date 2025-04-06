

import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    world.add_component(input_left, CInputCommand(name="Player left",key=pygame.K_a,))
    