

import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    world.add_component(input_left, CInputCommand(name="PLAYER LEFT",key=pygame.K_a,))
    world.add_component(input_right, CInputCommand(name="PLAYER RIGHT",key=pygame.K_d,))
    world.add_component(input_up, CInputCommand(name="PLAYER UP",key=pygame.K_w,))
    world.add_component(input_down, CInputCommand(name="PLAYER DOWN",key=pygame.K_s,))
    