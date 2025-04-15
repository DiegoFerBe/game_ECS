

import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float) -> None:

    components = world.get_components(CAnimation, CSurface)

    for entity, (c_animation, c_surface) in components:
        c_animation.current_animation_time -= delta_time

        if c_animation.current_animation_time <= 0:
            c_animation.current_animation_time = c_animation.animations_list[c_animation.current_animation].framerate

            c_animation.current_frame += 1

            if c_animation.current_frame > c_animation.animations_list[c_animation.current_animation].end:
                c_animation.current_frame = c_animation.animations_list[c_animation.current_animation].start

            sprite_sheet = c_surface.surface.get_rect()
            c_surface.area.w = sprite_sheet.width // c_animation.number_frames
            c_surface.area.x = c_surface.area.w * c_animation.current_frame

def set_animation(animation:CAnimation, index_animation:int):
    if animation.current_animation != index_animation:
        animation.current_animation = index_animation
        animation.current_animation_time = 0.0
        animation.current_frame = animation.animations_list[animation.current_animation].start
            
