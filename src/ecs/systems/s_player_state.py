import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World):
    componentes = world.get_components(CVelocity, CAnimation, CPlayerState)
    for entity, (velocity, animation, player_state) in componentes:
        _update_player_state(velocity, animation, player_state)


def _update_player_state(velocity: CVelocity, animation: CAnimation, player_state: CPlayerState):
    _set_animation(animation, 0 if player_state.state == PlayerState.MOVE else 1)
    new_state = PlayerState.MOVE if velocity.velocity.magnitude_squared() > 0 else PlayerState.IDLE

    if player_state.state != new_state:
        player_state.state = new_state
        _set_animation(animation, 0 if new_state == PlayerState.MOVE else 1)

def _set_animation(animation:CAnimation, index_animation:int):
    if animation.current_animation != index_animation:
        animation.current_animation = index_animation
        animation.current_animation_time = 0.0
        animation.current_frame = animation.animations_list[animation.current_animation].start
       