import math
import random
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def create_rectangle(world:esper.World,size:pygame.Vector2,color:pygame.Color,position:pygame.Vector2,velocity:pygame.Vector2) -> None:
    rectangle_entity = world.create_entity()
    world.add_component(rectangle_entity,
                        CSurface(size=size,color=color))
    world.add_component(rectangle_entity,
                        CTransform(position=position))
    world.add_component(rectangle_entity,
                        CVelocity(velocity=velocity))
    
def create_enemy_rectangle(world:esper.World,cfg_enemy:dict,position:pygame.Vector2) -> None:
    size = pygame.Vector2(cfg_enemy['size']['x'], cfg_enemy['size']['y'])
    color = pygame.Color(cfg_enemy['color']['r'], cfg_enemy['color']['g'], cfg_enemy['color']['b'])

    angle = random.uniform(0, 360)
    angle_rad = math.radians(angle)
    velocity_min = pygame.Vector2(100,100)
    velocity_min:float = cfg_enemy['velocity_min']
    velocity_max:float = cfg_enemy['velocity_max']
    velocity = random.uniform(velocity_min, velocity_max)
    create_rectangle(
                world=world,
                size=size,
                color=color,
                position=position,
                velocity=pygame.Vector2(velocity * math.cos(angle_rad), velocity * math.sin(angle_rad)),
            )
    
def create_player_rectangle(world:esper.World,cfg_player:dict,position:dict) -> None:
    size = pygame.Vector2(cfg_player['size']['x'], cfg_player['size']['y'])
    color = pygame.Color(cfg_player['color']['r'], cfg_player['color']['g'], cfg_player['color']['b'])
    velocity = pygame.Vector2(0,0)
    position = pygame.Vector2(position['position']['x'], position['position']['y'])
    create_rectangle(
                world=world,
                size=size,
                color=color,
                position=position,
                velocity=velocity,
            )