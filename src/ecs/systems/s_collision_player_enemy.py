

import esper

from src.create.prefab_rectangle import create_explotion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_player_enemy(world:esper.World,player_entity:int, level_cfg:dict, cfg_explotion:dict) -> None:
    components = world.get_components(CSurface,CTransform,CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rectangle = player_surface.area.copy()
    player_rectangle.topleft = player_transform.position

    for enemy_entity, (surface, transform, tag_enemy) in components:

        enemy_rectangle = surface.area.copy()
        enemy_rectangle.topleft = transform.position

        if player_rectangle.colliderect(enemy_rectangle):
            world.delete_entity(enemy_entity)
            create_explotion(world,cfg_explotion, transform.position)

            player_transform.position.y = level_cfg['player_spawn']['position']['y'] - player_rectangle.height / 2
            player_transform.position.x = level_cfg['player_spawn']['position']['x'] - player_rectangle.width / 2