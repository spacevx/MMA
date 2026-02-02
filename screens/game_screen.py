import random
from pathlib import Path
from typing import Callable

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.sprite import Group

from settings import GameState, ScreenSize, WIDTH, HEIGHT, WHITE
from entities import Player, Chaser, Obstacle
from strings import GAME_OVER, GAME_RESTART

ASSETS_PATH: Path = Path(__file__).parent


class GameScreen:
    def __init__(self, set_state_callback: Callable[[GameState], None]) -> None:
        self.set_state: Callable[[GameState], None] = set_state_callback
        self.screen_size: ScreenSize = (WIDTH, HEIGHT)

        self._load_background()

        self.scroll_x: float = 0.0
        self.scroll_speed: float = 300.0

        self.ground_y: int = int(HEIGHT * 0.90)
        self.lanes: list[int] = self._calculate_lanes()

        self.player: Player = Player(180, self.lanes[2])
        self.player.set_lanes(self.lanes)

        self.chaser: Chaser = Chaser(-50, self.lanes[2])
        self.chaser.speed = 180.0

        self.all_sprites: Group = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.chaser)

        self.obstacles: Group = pygame.sprite.Group()
        self.obstacle_timer: float = 0.0
        self.obstacle_spawn_delay: float = 2.0
        self.last_obstacle_lane: int = -1

        self.hits: int = 0
        self.max_hits: int = 2
        self.invincible_timer: float = 0.0
        self.invincible_duration: float = 1.5

        self.game_over: bool = False
        self.font: pygame.font.Font = pygame.font.Font(None, 72)
        self.small_font: pygame.font.Font = pygame.font.Font(None, 36)

    def _calculate_lanes(self) -> list[int]:
        return [
            self.ground_y - 280,
            self.ground_y - 140,
            self.ground_y
        ]

    def _load_background(self) -> None:
        bg_path: Path = ASSETS_PATH / "background.png"
        original: Surface = pygame.image.load(str(bg_path)).convert()
        self.background: Surface = pygame.transform.scale(
            original,
            (self.screen_size[0], self.screen_size[1])
        )
        self.bg_width: int = self.background.get_width()

    def on_resize(self, new_size: ScreenSize) -> None:
        self.screen_size = new_size
        self._load_background()
        self.ground_y = int(new_size[1] * 0.90)
        self.lanes = self._calculate_lanes()
        self.player.set_lanes(self.lanes)
        self.player.set_screen_size(new_size)
        self.chaser.set_screen_size(new_size)

    def reset(self) -> None:
        self.ground_y = int(self.screen_size[1] * 0.90)
        self.lanes = self._calculate_lanes()

        self.player.set_lanes(self.lanes)
        self.player.rect.center = (180, self.lanes[2])
        self.player.current_lane = 2
        self.player.target_y = float(self.lanes[2])

        self.chaser.rect.center = (-50, self.lanes[2])
        self.chaser.speed = 180.0

        self.scroll_x = 0.0
        self.hits = 0
        self.invincible_timer = 0.0
        self.game_over = False
        self.obstacle_timer = 0.0
        self.last_obstacle_lane = -1

        for obstacle in self.obstacles:
            obstacle.kill()

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset()
            elif not self.game_over:
                self.player.handle_input(event)

    def _spawn_obstacle(self) -> None:
        x: int = self.screen_size[0] + 100

        available_lanes: list[int] = [0, 1, 2]
        if self.last_obstacle_lane >= 0:
            available_lanes = [i for i in available_lanes if i != self.last_obstacle_lane]

        lane_idx: int = random.choice(available_lanes)
        self.last_obstacle_lane = lane_idx

        lane_y: int = self.lanes[lane_idx]
        obstacle: Obstacle = Obstacle(x, lane_y)
        obstacle.speed = self.scroll_speed
        self.obstacles.add(obstacle)

    def _check_collisions(self) -> None:
        if self.invincible_timer > 0:
            return

        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                self.hits += 1
                self.invincible_timer = self.invincible_duration
                self.chaser.speed += 60.0
                self.chaser.rect.x += 100
                obstacle.kill()

                if self.hits >= self.max_hits:
                    self.game_over = True
                break

        if self.player.rect.colliderect(self.chaser.rect):
            self.game_over = True

    def update(self, dt: float) -> None:
        if self.game_over:
            return

        self.scroll_x += self.scroll_speed * dt
        if self.scroll_x >= self.bg_width:
            self.scroll_x -= self.bg_width

        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        self.player.update(dt)

        target_x: int = self.player.rect.centerx - 250
        target_y: int = self.player.rect.centery
        self.chaser.set_target(target_x, target_y)
        self.chaser.update(dt)

        self.obstacle_timer += dt
        if self.obstacle_timer >= self.obstacle_spawn_delay:
            self._spawn_obstacle()
            self.obstacle_timer = 0.0
            self.obstacle_spawn_delay = random.uniform(1.5, 2.5)

        for obstacle in self.obstacles:
            obstacle.update(dt)
            if obstacle.is_off_screen():
                obstacle.kill()

        self._check_collisions()

    def draw(self, screen: Surface) -> None:
        x1: int = -int(self.scroll_x)
        x2: int = x1 + self.bg_width

        screen.blit(self.background, (x1, 0))
        screen.blit(self.background, (x2, 0))

        for obstacle in self.obstacles:
            screen.blit(obstacle.image, obstacle.rect)

        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2 == 0:
            pass
        else:
            screen.blit(self.player.image, self.player.rect)

        screen.blit(self.chaser.image, self.chaser.rect)

        self._draw_ui(screen)

        if self.game_over:
            self._draw_game_over(screen)

    def _draw_ui(self, screen: Surface) -> None:
        hits_text: str = f"Vies: {self.max_hits - self.hits}/{self.max_hits}"
        text_surface: Surface = self.small_font.render(hits_text, True, WHITE)
        screen.blit(text_surface, (20, 20))

    def _draw_game_over(self, screen: Surface) -> None:
        overlay: Surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        text: Surface = self.font.render(GAME_OVER, True, (255, 50, 50))
        text_rect = text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 - 30))
        screen.blit(text, text_rect)

        restart_text: Surface = self.small_font.render(GAME_RESTART, True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + 30))
        screen.blit(restart_text, restart_rect)
