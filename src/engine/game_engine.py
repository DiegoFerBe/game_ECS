import pygame
import esper

from src.create.prefab_rectangle import create_player_rectangle
from src.create.prefab_spawner import create_spawner
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

        self.level_config = load_json("assets/cfg/level_01.json")
        self.enemies = load_json("assets/cfg/enemies.json")
        self.window_config = load_json("assets/cfg/window.json")
        self.player_config = load_json("assets/cfg/player.json")


        self.fps = self.window_config["framerate"]
        # Create the main screen
        self.screen = pygame.display.set_mode((self.window_config["size"]["w"], self.window_config["size"]["h"]))
        pygame.display.set_caption(self.window_config["title"])

        


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
        #Enemy spawner
        create_spawner(self.world, self.level_config["enemy_spawn_events"])
        # Player
        create_player_rectangle(self.world, self.player_config, self.level_config["player_spawn"])

        


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
        self.screen.fill((self.window_config["bg_color"]["r"], self.window_config["bg_color"]["g"], self.window_config["bg_color"]["b"]))
        system_rendering(self.world,self.screen)

        # custom debug system
        system_debug(self.world,self.screen)

        pygame.display.flip()

    def _clean(self):
        pygame.quit()
