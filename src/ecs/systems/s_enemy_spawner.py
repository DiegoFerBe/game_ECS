import math
from typing import Dict, List
import esper
import pygame
import random

from src.create.prefab_rectangle import create_enemy_rectangle
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world:esper.World,delta_time: float, enemy_types: list[Dict]) -> None:
    components = world.get_component(CEnemySpawner)

    ent, spawner = components[0]
    spawner.timer += delta_time
    while spawner.current_index < len(spawner.spawn_events):
        event = spawner.spawn_events[spawner.current_index]
        time = event['time']
        enemy_type = event['enemy_type']
        position = pygame.Vector2(event['position']['x'], event['position']['y'])
        
        if spawner.timer >= time:
            type_data = enemy_types[enemy_type]
            create_enemy_rectangle(
                world=world,
                cfg_enemy=type_data,
                position=position
            )
            spawner.current_index += 1
        else:
            break
