from typing import Dict, List
import pygame
import esper

from src.create.prefab_rectangle import create_rectangle
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_debug import system_debug
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.utils.json_loader import load_json

class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.delta_time = 0.0

        # Square properties
        self.square_position = pygame.Vector2(150, 50)
        self.square_size = pygame.Vector2(50, 50)
        self.square_color = pygame.Color(255, 0, 0)
        self.square_speed = pygame.Vector2(100, 100)
        self.world = esper.World()


        


    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        #create_rectangle(self.world,self.square_size, self.square_color, self.square_position, self.square_speed)

        self.spawners = load_json("src/cfg/level_01.json","enemy_spawn_events")
        self.enemies = load_json("src/cfg/enemies.json")
        self.main_config = load_json("src/cfg/window.json")

        self.fps = self.main_config["framerate"]


        #Enemy spawner
        enemy_spawner = self.world.create_entity()
        self.world.add_component(enemy_spawner, CEnemySpawner(self.spawners))

        # Create the main screen
        self.screen = pygame.display.set_mode((self.main_config["size"]["w"], self.main_config["size"]["h"]))

        pygame.display.set_caption(self.main_config["title"])


    def _calculate_time(self):
        self.clock.tick(self.fps)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.world,self.delta_time)
        system_screen_bounce(self.world,self.screen)
        system_enemy_spawner(self.world,self.delta_time, self.enemies)

    def _draw(self):
        self.screen.fill((self.main_config["bg_color"]["r"], self.main_config["bg_color"]["g"], self.main_config["bg_color"]["b"]))
        system_rendering(self.world,self.screen)

        # custom debug system
        system_debug(self.world,self.screen)

        pygame.display.flip()

    def _clean(self):
        pygame.quit()
