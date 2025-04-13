
import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_hunter_state(world: esper.World, player_entity: int, cfg_hunter: dict, delta_time: float) -> None:
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_center = player_transform.position + pygame.Vector2(
        player_surface.area.width / 2,
        player_surface.area.height / 2
    )
    velocity: CVelocity
    transform: CTransform
    animation: CAnimation
    hunter_state: CHunterState
    tag_enemy: CTagEnemy
    components = world.get_components(CVelocity, CTransform, CSurface, CAnimation, CHunterState, CTagEnemy)
    for entity, (velocity, transform,surface, animation, hunter_state, tag_enemy) in components:
        _update_hunter_state(velocity, transform, surface, player_center, cfg_hunter, delta_time)
        _update_hunter_animation(velocity,animation, hunter_state)


def _update_hunter_state(velocity: CVelocity, transform: CTransform, surface: CSurface, 
                         player_center: pygame.Vector2, cfg_hunter: dict, delta_time: float) -> None:
    
    position_enemy = transform.position + pygame.Vector2(
        surface.area.width / 2,
        surface.area.height / 2
    )
    spawn_position = transform.spawn_position + pygame.Vector2(
        surface.area.width / 2,
        surface.area.height / 2
    )
    distance_to_player = _truncate_vector(player_center - position_enemy,0)
    distance_to_spawn = _truncate_vector(spawn_position - position_enemy,0)

    distance_to_player_length = distance_to_player.length()
    distance_to_spawn_length = round(distance_to_spawn.length(),0)

    velocity_chase = cfg_hunter["velocity_chase"]
    velocity_return = cfg_hunter["velocity_return"]

    if cfg_hunter["distance_start_chase"] >= distance_to_player_length < cfg_hunter["distance_start_return"]:
        velocity.velocity = distance_to_player.normalize() * velocity_chase * delta_time
        transform.position += velocity.velocity
    else:
        print(f"distance_to_spawn_length: {distance_to_spawn_length}")
        if distance_to_spawn_length <= 1.0:
            velocity.velocity = pygame.Vector2(0, 0)
            return
        velocity.velocity = distance_to_spawn.normalize() * velocity_return * delta_time
        transform.position += velocity.velocity
   
    


def _update_hunter_animation(velocity:CVelocity,animation: CAnimation, state: CHunterState) -> None:
    _set_animation(animation, 0 if state.state == HunterState.MOVE else 1)
    new_state = HunterState.MOVE if velocity.velocity.magnitude_squared() > 0 else HunterState.IDLE

    if state.state != new_state:
        state.state = new_state
        _set_animation(animation, 0 if new_state == HunterState.MOVE else 1)


def _set_animation(animation:CAnimation, index_animation:int):
    if animation.current_animation != index_animation:
        animation.current_animation = index_animation
        animation.current_animation_time = 0.0
        animation.current_frame = animation.animations_list[animation.current_animation].start

def _truncate_vector(vector: pygame.Vector2, decimals: int) -> pygame.Vector2:
    return pygame.Vector2(round(vector.x, decimals), round(vector.y, decimals))