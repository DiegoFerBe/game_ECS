

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet(world: esper.World,screen: pygame.Surface ,max_bullets_in_screen: int) -> None:
    components = world.get_components(CTransform, CVelocity, CSurface, CTagBullet)

    to_delete = set()

    for entity, (c_t, c_v, c_s, c_b) in components:
        bullet_rect = c_s.surface.get_rect(topleft=c_t.position)

        if not screen.get_rect().colliderect(bullet_rect):
            to_delete.add(entity)

    if len(components) > max_bullets_in_screen:
        last_entity = list(components)[-1][0]
        to_delete.add(last_entity)

    for entity in to_delete:
        world.delete_entity(entity)