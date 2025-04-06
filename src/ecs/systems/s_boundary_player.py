

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_boundary_player(world: esper.World,screen:pygame.surface):
    # screen_rectangle = screen.get_rect()
    # components = world.get_components(CTransform, CSurface, CTagPlayer)

    # for entity, (c_t, c_s, _) in components:
    #     sprite_rect = c_s.surface.get_rect(topleft=c_t.position)

    #     # Eje X
    #     if sprite_rect.left < 0:
    #         c_t.position.x = 0
    #     elif sprite_rect.right > screen_rectangle.width:
    #         c_t.position.x = screen_rectangle.width - sprite_rect.width

    #     # Eje Y
    #     if sprite_rect.top < 0:
    #         c_t.position.y = 0
    #     elif sprite_rect.bottom > screen_rectangle.height:
    #         c_t.position.y = screen_rectangle.height - sprite_rect.height
    screen_rectangle = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayer)

    for entity, (c_t, c_s, _) in components:
        sprite_rect = c_s.surface.get_rect(topleft=c_t.position)

        # Corrección eje X
        if sprite_rect.left < 0:
            c_t.position.x = 0
        elif sprite_rect.right > screen_rectangle.width:
            c_t.position.x = screen_rectangle.width - sprite_rect.width

        # Corrección eje Y
        if sprite_rect.top < 0:
            c_t.position.y = 0
        elif sprite_rect.bottom > screen_rectangle.height:
            c_t.position.y = screen_rectangle.height - sprite_rect.height

        # Recalcular el rect con la posición actual
        corrected_rect = c_s.surface.get_rect(topleft=c_t.position)

        # Seguridad: aplicar clamp solo si realmente está fuera de los límites
        if not screen_rectangle.contains(corrected_rect):
            corrected_rect.clamp_ip(screen_rectangle)
            c_t.position.x = corrected_rect.x
            c_t.position.y = corrected_rect.y