import esper
import pygame

from src.ecs.components.c_state_ui import CStateUI
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator

def system_rendering(world:esper.World,screen:pygame.Surface) -> None:
    components = world.get_components(CTransform,CSurface)

    c_t:CTransform
    c_s:CSurface
    for entity,(c_t,c_s) in components:
        screen.blit(c_s.surface,c_t.position,area=c_s.area)

    components_text = world.get_components(CText, CTransform, CStateUI)
    for entity, (c_text, c_transform,c_state) in components_text:
        text_surface = c_text.font.render(c_text.text, True, c_text.color)
        if c_state.state:
            screen.blit(text_surface, c_transform.position)