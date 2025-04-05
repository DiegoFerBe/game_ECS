import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(world:esper.World,delta_time:float):
    components = world.get_components(CTransform,CVelocity)
    
    c_t: CTransform
    c_v:CVelocity

    for entity,(c_t,c_v) in components:
        c_t.position.x += c_v.velocity.x * delta_time
        c_t.position.y += c_v.velocity.y * delta_time
  