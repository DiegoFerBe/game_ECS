

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_debug(world:esper.World, screen:pygame.Surface) -> None:

    components = world.get_components(CTransform,CSurface,CVelocity)  

    font = pygame.font.Font(None, 33)
    debug_info = f"Entities: {len(components)}"
    
    # Render the debug information
    text_surface = font.render(debug_info, True, pygame.Color(255, 255, 255))
    screen.blit(text_surface, (10, 10))  # Position the text at (10, 10)

    c_t:CTransform
    c_s:CSurface
    for entity, (c_t, c_s,c_v) in components:
        
        entity_rect = c_s.area.copy()
        entity_rect.topleft = c_t.position

        # Dibujar rectángulo de colisión
        pygame.draw.rect(screen, (255, 0, 0), entity_rect, 1)

        # Coordenadas izquierda y derecha con respecto a la posición en pantalla
        left_x = entity_rect.left
        right_x = entity_rect.right
        top_y = entity_rect.centery

        # Renderizar texto en la posición del sprite
        font = pygame.font.Font(None, 12)
        text_surface_1 = font.render(f"left: {left_x}", True, (255, 255, 255))  
        text_surface_2 = font.render(f"right: {right_x}", True, (255, 255, 255))
        text_surface_3 = font.render(f"v: {c_v.velocity}", True, (255, 255, 255))  

        # Posicionar texto cerca de los lados
        #screen.blit(text_surface_1, (left_x, top_y))   # Izquierda
        #screen.blit(text_surface_2, (right_x, top_y))   # Posiciona el texto cerca del punto
        screen.blit(text_surface_3, (entity_rect.centerx, entity_rect.centery))   # Posiciona el texto cerca del punto
