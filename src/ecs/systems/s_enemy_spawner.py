import math
from typing import Dict, List
import esper
import pygame
import random

from src.create.prefab_rectangle import create_rectangle
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world:esper.World,delta_time: float, enemy_types: Dict) -> None:
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
            size = pygame.Vector2(type_data['size']['x'], type_data['size']['y'])
            color = pygame.Color(type_data['color']['r'], type_data['color']['g'], type_data['color']['b'])

            angle = random.uniform(0, 360)
            angle_rad = math.radians(angle)
            velocity_min = pygame.Vector2(100,100)
            velocity_min:float = type_data['velocity_min']
            velocity_max:float = type_data['velocity_max']

            velocity = random.uniform(velocity_min, velocity_max)
            
            create_rectangle(
                world=world,
                size=size,
                color=color,
                position=position,
                velocity=pygame.Vector2(velocity * math.cos(angle_rad), velocity * math.sin(angle_rad)),
            )
            spawner.current_index += 1
        else:
            break
