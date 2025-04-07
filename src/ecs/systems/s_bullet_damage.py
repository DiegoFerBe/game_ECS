

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_bullet_damage_enemies(world: esper.World) -> None:
    """
    This system handles the damage to enemies from bullets.
    It checks for collisions between bullets and enemies and applies damage accordingly.
    """
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)

    to_delete_bullets = set()
    to_delete_enemies = set()

    for bullet_entity, (c_b_surface, c_b_transform, _) in bullets:
        bullet_rect = c_b_surface.surface.get_rect(topleft=c_b_transform.position)

        for enemy_entity, (c_e_surface, c_e_transform, _) in enemies:
            enemy_rect = c_e_surface.surface.get_rect(topleft=c_e_transform.position)

            if bullet_rect.colliderect(enemy_rect):
                to_delete_bullets.add(bullet_entity)
                to_delete_enemies.add(enemy_entity)
                break

    for bullet_entity in to_delete_bullets:
        world.delete_entity(bullet_entity)
    
    for enemy_entity in to_delete_enemies:
        world.delete_entity(enemy_entity)