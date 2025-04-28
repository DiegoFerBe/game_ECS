

import esper
import pygame

from src.create.prefab_rectangle import create_explotion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
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

def system_camouflage(game_engine, world: esper.World, duration_text: int) -> None:
    if game_engine.is_camouflage and not game_engine.is_reloading_camouflage:
        game_engine.camouflage_duration -= game_engine.delta_time
        if game_engine.camouflage_duration <= 0:
            game_engine.is_camouflage = False
            game_engine.is_reloading_camouflage = True
            game_engine.camouflage_reload_timer = 5.0 
            game_engine.camouflage_duration = 0.0

    elif game_engine.is_reloading_camouflage:
        game_engine.camouflage_reload_timer -= game_engine.delta_time
        if game_engine.camouflage_reload_timer <= 0:
            game_engine.is_reloading_camouflage = False

    camouflage_text = world.component_for_entity(duration_text, CText)
    if game_engine.is_camouflage:
        camouflage_text.text = f"Time camouflage: {game_engine.camouflage_duration:.1f}s"
        camouflage_text.color = pygame.color.Color(0, 255, 0)
    elif game_engine.is_reloading_camouflage:
        reload_percentage = 100 - int((game_engine.camouflage_reload_timer / 5.0) * 100)
        camouflage_text.text = f"Reloading: {reload_percentage}%"
        camouflage_text.color = pygame.color.Color(255, 0, 0)
    else:
        camouflage_text.text = "Camouflage: Ready"
        camouflage_text.color = pygame.color.Color(255, 255, 255)