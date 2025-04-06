import pygame
import esper

from src.create.prefab_creator import create_input_player
from src.create.prefab_rectangle import create_player_rectangle
from src.create.prefab_spawner import create_spawner
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_boundary_player import system_boundary_player
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_debug import system_debug
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
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

        create_input_player(self.world)

        # Player
        self._player_entity = create_player_rectangle(self.world, self.player_config, self.level_config["player_spawn"])
        self._player_c_velocity = self.world.component_for_entity(self._player_entity, CVelocity)

        


    def _calculate_time(self):
        self.clock.tick(self.fps)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.world,self.delta_time)
        #system_screen_bounce(self.world,self.screen)
        system_boundary_player(self.world,self.screen)
        #system_enemy_spawner(self.world,self.delta_time, self.enemies)
        #system_collision_player_enemy(self.world,self._player_entity, self.level_config)
        self.world._clear_dead_entities()

    def _draw(self):
        self.screen.fill((self.window_config["bg_color"]["r"], self.window_config["bg_color"]["g"], self.window_config["bg_color"]["b"]))
        system_rendering(self.world,self.screen)

        # custom debug system
        system_debug(self.world,self.screen)

        pygame.display.flip()

    def _clean(self):
        self.world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.velocity.x -= self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.velocity.x += self.player_config["input_velocity"]

        if c_input.name == "PLAYER RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.velocity.x += self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.velocity.x -= self.player_config["input_velocity"]
        
        if c_input.name == "PLAYER UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.velocity.y -= self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.velocity.y += self.player_config["input_velocity"]

        if c_input.name == "PLAYER DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.velocity.y += self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.velocity.y -= self.player_config["input_velocity"]
            
