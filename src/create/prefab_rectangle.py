import math
import random
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def create_rectangle(world:esper.World,size:pygame.Vector2,color:pygame.Color,position:pygame.Vector2,velocity:pygame.Vector2) -> int:
    rectangle_entity = world.create_entity()
    world.add_component(rectangle_entity,
                        CSurface(size=size,color=color))
    world.add_component(rectangle_entity,
                        CTransform(position=position))
    world.add_component(rectangle_entity,
                        CVelocity(velocity=velocity))
    return rectangle_entity
    
def create_enemy_rectangle(world:esper.World,cfg_enemy:dict,position:pygame.Vector2) -> None:
    size = pygame.Vector2(cfg_enemy['size']['x'], cfg_enemy['size']['y'])
    color = pygame.Color(cfg_enemy['color']['r'], cfg_enemy['color']['g'], cfg_enemy['color']['b'])

    angle = random.uniform(0, 360)
    angle_rad = math.radians(angle)
    velocity_min = pygame.Vector2(100,100)
    velocity_min:float = cfg_enemy['velocity_min']
    velocity_max:float = cfg_enemy['velocity_max']
    velocity = random.uniform(velocity_min, velocity_max)
    enemy_entity:int = create_rectangle(
                world=world,
                size=size,
                color=color,
                position=position,
                velocity=pygame.Vector2(velocity * math.cos(angle_rad), velocity * math.sin(angle_rad)),
            )
    world.add_component(enemy_entity,CTagEnemy())
    return enemy_entity
    
def create_player_rectangle(world:esper.World,cfg_player:dict,position:dict) -> int:
    size = pygame.Vector2(cfg_player['size']['x'], cfg_player['size']['y'])
    color = pygame.Color(cfg_player['color']['r'], cfg_player['color']['g'], cfg_player['color']['b'])
    velocity = pygame.Vector2(0,0)
    position = pygame.Vector2(position['position']['x'] - size.x / 2, position['position']['y'] - size.y / 2)
    player_entity:int = create_rectangle(
                world=world,
                size=size,
                color=color,
                position=position,
                velocity=velocity,
            )
    
    world.add_component(player_entity,CTagPlayer())
    return player_entity

def create_bullet_rectangle(world:esper.World,cfg_bullet:dict,position:pygame.Vector2,positionScope: pygame.Vector2) -> int:
    size = pygame.Vector2(cfg_bullet['size']['x'], cfg_bullet['size']['y'])
    color = pygame.Color(cfg_bullet['color']['r'],
                         cfg_bullet['color']['g'],
                         cfg_bullet['color']['b'])

    direction = (positionScope - position)
    if direction.length_squared() > 0:  # Evita división por 0
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)  # Dirección por defecto si son iguales

    # Multiplicar dirección por velocidad
    speed = cfg_bullet["velocity"]
    velocity = direction * speed

    # Crear la bala
    bullet_entity: int = create_rectangle(
        world=world,
        size=size,
        color=color,
        position=position,
        velocity=velocity,
    )

    world.add_component(bullet_entity, CTagBullet())

    return bullet_entity