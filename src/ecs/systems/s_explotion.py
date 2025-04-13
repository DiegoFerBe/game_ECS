

import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explotion import CTagExplotion


def system_explotion(world: esper.World) -> None:
    components = world.get_components(CAnimation,CTagExplotion)
    for entity, (animation, _) in components:
        if animation.current_frame >= animation.number_frames-1:
            world.delete_entity(entity)
            continue

