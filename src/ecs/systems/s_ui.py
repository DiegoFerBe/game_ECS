
import esper
import pygame

from src.ecs.components.c_state_ui import CStateUI
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_ui import CTagUI, UIType


def system_ui(world: esper.World, world_state:bool) -> None:
    components_ui = world.get_components(CStateUI, CTagUI)
    for entity, (c_state_ui, c_tag_ui) in components_ui:
        if c_tag_ui.type == UIType.PAUSE:
            c_state_ui.state = world_state # Mostrar solo si el juego está en pausa
        elif c_tag_ui.type == UIType.GAMEPLAY:
            c_state_ui.state = not world_state



    