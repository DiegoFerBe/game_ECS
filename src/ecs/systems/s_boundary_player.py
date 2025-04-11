

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_boundary_player(world: esper.World, screen: pygame.Surface):
    screen_rectangle = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayer)

    for entity, (c_t, c_s, _) in components:
        sprite_rect = c_s.area.copy()
        sprite_rect.topleft = c_t.position

        if sprite_rect.left < 0:
            c_t.position.x = 0
        elif sprite_rect.right > screen_rectangle.width:
            c_t.position.x = screen_rectangle.width - sprite_rect.width

        if sprite_rect.top < 0:
            c_t.position.y = 0
        elif sprite_rect.bottom > screen_rectangle.height:
            c_t.position.y = screen_rectangle.height - sprite_rect.height