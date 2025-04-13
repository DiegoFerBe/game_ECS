import math
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CEnemyType, CTagEnemy
from src.ecs.components.tags.c_tag_explotion import CTagExplotion
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
    
    if "animations" in cfg_enemy:
        _create_animated_enemy(world, cfg_enemy, position)
    else:
        _create_standard_enemy(world, cfg_enemy, position)

def _create_standard_enemy(world: esper.World, cfg_enemy: dict, position: pygame.Vector2) -> None:
    enemy_surface = pygame.image.load(cfg_enemy['image']).convert_alpha()

    angle = random.uniform(0, 360)
    angle_rad = math.radians(angle)
    velocity_min = cfg_enemy['velocity_min']
    velocity_max = cfg_enemy['velocity_max']
    velocity = random.uniform(velocity_min, velocity_max)

    enemy_entity: int = create_sprite(
        world=world,
        position=position,
        velocity=pygame.Vector2(velocity * math.cos(angle_rad), velocity * math.sin(angle_rad)),
        texture=enemy_surface,
    )
    world.add_component(enemy_entity, CTagEnemy())
    return enemy_entity


def _create_animated_enemy(world: esper.World, cfg_enemy: dict, position: pygame.Vector2) -> None:
    enemy_sprite = pygame.image.load(cfg_enemy['image']).convert_alpha()

    size = enemy_sprite.get_rect()
    size.width = size.width / cfg_enemy['animations']['number_frames']
    
    velocity = pygame.Vector2(0, 0)
    #position = pygame.Vector2(position.x - size.width / 2, position.y - size.height / 2)

    enemy_entity: int = create_sprite(
        world=world,
        position=position,
        velocity=velocity,
        texture=enemy_sprite,
    )

    # Agregar componentes de animación y etiqueta de enemigo
    world.add_component(enemy_entity, CAnimation(cfg_enemy['animations']))
    world.add_component(enemy_entity, CHunterState())   
    world.add_component(enemy_entity, CTagEnemy(type=CEnemyType.HUNTER))
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
    size = bullet_sprite.get_rect()

    direction = (positionScope - position)
    if direction.length_squared() > 0: 
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)

    speed = cfg_bullet["velocity"]
    velocity = direction * speed

    position.x -= size.width / 2
    position.y -= size.height / 2

    bullet_entity: int = create_sprite(
        world=world,
        position=position,
        velocity=velocity,
        texture=bullet_sprite,
    )

    world.add_component(bullet_entity, CTagBullet())

    return bullet_entity

def create_explotion(world:esper.World,cfg_explotion:dict,position:pygame.Vector2) -> int:
    
    explotion_sprite = pygame.image.load(cfg_explotion['image']).convert_alpha()
    size = explotion_sprite.get_rect()
    size.width = size.width / cfg_explotion['animations']['number_frames']
    velocity = pygame.Vector2(0,0)
    position = pygame.Vector2(position.x - size.width / 2, position.y - size.height / 2)
    explotion_entity:int = create_sprite(
                world=world,
                position=position,
                velocity=velocity,
                texture=explotion_sprite,
            )
    
    world.add_component(explotion_entity,
                        CAnimation(cfg_explotion['animations']))
    world.add_component(explotion_entity,
                        CTagExplotion())
    
    return explotion_entity