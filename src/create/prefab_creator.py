

import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_shoot = world.create_entity()
    input_pause = world.create_entity()
    world.add_component(input_left, CInputCommand(name="PLAYER LEFT",key=pygame.K_LEFT,))
    world.add_component(input_right, CInputCommand(name="PLAYER RIGHT",key=pygame.K_RIGHT,))
    world.add_component(input_up, CInputCommand(name="PLAYER UP",key=pygame.K_UP,))
    world.add_component(input_down, CInputCommand(name="PLAYER DOWN",key=pygame.K_DOWN,))
    world.add_component(input_shoot, CInputCommand(name="PLAYER FIRE",key=1))
    world.add_component(input_pause, CInputCommand(name="PAUSE GAME",key=pygame.K_ESCAPE,))
    