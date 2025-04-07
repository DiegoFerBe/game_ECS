

from typing import Callable, Optional
import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player(world: esper.World,
                        event: pygame.event.Event,
                        do_action: Callable[[CInputCommand, Optional[pygame.Vector2]], None]):
    components = world.get_component(CInputCommand)
    mouse_pos = None

    if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
        phase = CommandPhase.START
    elif event.type in (pygame.KEYUP, pygame.MOUSEBUTTONUP):
        phase = CommandPhase.END
    else:
        return 

    if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    for entity, c_input in components:
        if (event.type in (pygame.KEYDOWN, pygame.KEYUP) and c_input.key == event.key) or \
           (event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP) and c_input.key == event.button):
            c_input.phase = phase
            do_action(c_input, mouse_pos)