import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world:esper.World):
    componentes = world.get_components(CVelocity,CAnimation,CPlayerState)
    for entity, (velocity, animation, player_state) in componentes:
        if player_state.state == PlayerState.IDLE:
            _do_idle_state(velocity, animation, player_state)
        elif player_state.state == PlayerState.MOVE:
            _do_move_state(velocity, animation, player_state)



def _do_idle_state(velocity:CVelocity, animation:CAnimation, player_state:CPlayerState):
    _set_animation(animation,1)
    if velocity.velocity.magnitude_squared() > 0:
        player_state.state = PlayerState.MOVE

def _do_move_state(velocity:CVelocity, animation:CAnimation, player_state:CPlayerState):
    _set_animation(animation,0)
    if velocity.velocity.magnitude_squared() <= 0:
        player_state.state = PlayerState.IDLE

def _set_animation(animation:CAnimation, index_animation:int):
    if animation.current_animation != index_animation:
        animation.current_animation = index_animation
        animation.current_animation_time = 0.0
        animation.current_frame = animation.animations_list[animation.current_animation].start
       