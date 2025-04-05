
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def create_spawner(world:esper.World, spawner_config:dict) -> None:
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(spawner_config))