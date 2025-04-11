import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_screen_bounce (world:esper.World,screen:pygame.surface):
    screen_rectangle = screen.get_rect()
    components = world.get_components(CTransform,CVelocity,CSurface,CTagEnemy)

    c_t: CTransform
    c_v:CVelocity
    c_s:CSurface
    for entity, (c_t,c_v,c_s,c_e) in components:
        entity_sprite = c_s.area.copy()
        entity_sprite.topleft = c_t.position

        if entity_sprite.left < 0 or entity_sprite.right > screen_rectangle.width:
            c_v.velocity.x *= -1
            entity_sprite.clamp_ip(screen_rectangle)
            c_t.position.x = entity_sprite.x
        if entity_sprite.top < 0 or entity_sprite.bottom > screen_rectangle.height:
            c_v.velocity.y *= -1
            entity_sprite.clamp_ip(screen_rectangle)
            c_t.position.y = entity_sprite.y
