import math
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
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

def create_sprite(world:esper.World,position:pygame.Vector2,velocity:pygame.Vector2,texture:pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(position=position))
    world.add_component(sprite_entity,
                        CVelocity(velocity=velocity))
    world.add_component(sprite_entity,
                        CSurface.from_surface(texture))
    return sprite_entity
    
def create_enemy_rectangle(world:esper.World,cfg_enemy:dict,position:pygame.Vector2) -> None:
    
    enemy_surface = pygame.image.load(cfg_enemy['image']).convert_alpha()

    angle = random.uniform(0, 360)
    angle_rad = math.radians(angle)
    velocity_min = pygame.Vector2(100,100)
    velocity_min:float = cfg_enemy['velocity_min']
    velocity_max:float = cfg_enemy['velocity_max']
    velocity = random.uniform(velocity_min, velocity_max)
    enemy_entity:int = create_sprite(
                world=world,
                position=position,
                velocity=pygame.Vector2(velocity * math.cos(angle_rad), velocity * math.sin(angle_rad)),
                texture=enemy_surface,
            )
    world.add_component(enemy_entity,CTagEnemy())
    return enemy_entity
    
def create_player_rectangle(world:esper.World,cfg_player:dict,position:dict) -> int:
    
    player_sprite = pygame.image.load(cfg_player['image']).convert_alpha()
    size = player_sprite.get_rect()
    size.width = size.width / cfg_player['animations']['number_frames']
    velocity = pygame.Vector2(0,0)
    position = pygame.Vector2(position['position']['x'] - size.width / 2, position['position']['y'] - size.height / 2)
    player_entity:int = create_sprite(
                world=world,
                position=position,
                velocity=velocity,
                texture=player_sprite,
            )
    
    world.add_component(player_entity,
                        CAnimation(cfg_player['animations']))
    
    world.add_component(player_entity,CTagPlayer())
    world.add_component(player_entity,
                        CPlayerState())
    return player_entity

def create_bullet_rectangle(world:esper.World,cfg_bullet:dict,position:pygame.Vector2,positionScope: pygame.Vector2) -> int:
    
    bullet_sprite = pygame.image.load(cfg_bullet['image']).convert_alpha()

    direction = (positionScope - position)
    if direction.length_squared() > 0:  # Evita división por 0
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)  # Dirección por defecto si son iguales

    speed = cfg_bullet["velocity"]
    velocity = direction * speed

    # Crear la bala
    bullet_entity: int = create_sprite(
        world=world,
        position=position,
        velocity=velocity,
        texture=bullet_sprite,
    )

    world.add_component(bullet_entity, CTagBullet())

    return bullet_entity