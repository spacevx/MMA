import random
from pathlib import Path
from typing import Callable

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.sprite import Group

from settings import GameState, ScreenSize, WIDTH, HEIGHT, WHITE, GOLD
from entities import Player, PlayerState, Chaser, Obstacle, ObstacleType
from strings import GAME_OVER, GAME_RESTART

ASSETS_PATH: Path = Path(__file__).parent


class GameScreen:
    SCROLL_SPEED: float = 400.0
    GROUND_RATIO: float = 0.85
    OBSTACLE_MIN_DELAY: float = 1.2
    OBSTACLE_MAX_DELAY: float = 2.5
    PLAYER_X: int = 250
    CHASER_START_X: int = -150

    def __init__(self, set_state_callback: Callable[[GameState], None]) -> None:
        self.set_state: Callable[[GameState], None] = set_state_callback
        self.screen_size: ScreenSize = (WIDTH, HEIGHT)

        Obstacle.clear_cache()
        self._load_background()

        self.scroll_x: float = 0.0
        self.scroll_speed: float = self.SCROLL_SPEED

        self.ground_y: int = int(HEIGHT * self.GROUND_RATIO)

        self.player: Player = Player(self.PLAYER_X, self.ground_y)
        self.chaser: Chaser = Chaser(self.CHASER_START_X, self.ground_y)

        self.all_sprites: Group = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.chaser)

        self.obstacles: Group = pygame.sprite.Group()
        self.obstacle_timer: float = 0.0
        self.obstacle_spawn_delay: float = 2.0
        self.last_obstacle_type: ObstacleType | None = None

        self.score: int = 0
        self.game_over: bool = False

        self.invincible_timer: float = 0.0
        self.invincible_duration: float = 1.0

        self.font: pygame.font.Font = pygame.font.Font(None, 72)
        self.small_font: pygame.font.Font = pygame.font.Font(None, 36)
        self.score_font: pygame.font.Font = pygame.font.Font(None, 48)

    def _load_background(self) -> None:
        bg_path: Path = ASSETS_PATH / "background.png"
        try:
            original: Surface = pygame.image.load(str(bg_path)).convert()
            self.background: Surface = pygame.transform.scale(
                original,
                (self.screen_size[0], self.screen_size[1])
            )
        except (pygame.error, FileNotFoundError):
            self.background = self._create_fallback_background()
        self.bg_width: int = self.background.get_width()

    def _create_fallback_background(self) -> Surface:
        surface: Surface = pygame.Surface(self.screen_size)
        surface.fill((135, 206, 235))
        ground_rect: pygame.Rect = pygame.Rect(
            0, int(self.screen_size[1] * self.GROUND_RATIO),
            self.screen_size[0], int(self.screen_size[1] * (1 - self.GROUND_RATIO))
        )
        pygame.draw.rect(surface, (34, 139, 34), ground_rect)
        return surface

    def on_resize(self, new_size: ScreenSize) -> None:
        self.screen_size = new_size
        self._load_background()
        self.ground_y = int(new_size[1] * self.GROUND_RATIO)
        self.player.set_screen_size(new_size)
        self.player.set_ground_y(self.ground_y)
        self.chaser.set_screen_size(new_size)
        self.chaser.set_ground_y(self.ground_y)

    def reset(self) -> None:
        Obstacle.clear_cache()
        self.ground_y = int(self.screen_size[1] * self.GROUND_RATIO)

        self.player = Player(self.PLAYER_X, self.ground_y)
        self.player.set_screen_size(self.screen_size)

        self.chaser = Chaser(self.CHASER_START_X, self.ground_y)
        self.chaser.set_screen_size(self.screen_size)

        self.all_sprites.empty()
        self.all_sprites.add(self.player, self.chaser)

        for obstacle in self.obstacles:
            obstacle.kill()
        self.obstacles.empty()

        self.scroll_x = 0.0
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0.0
        self.obstacle_spawn_delay = 2.0
        self.last_obstacle_type = None
        self.invincible_timer = 0.0

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset()
            elif not self.game_over:
                self.player.handle_input(event)

    def _spawn_obstacle(self) -> None:
        x: int = self.screen_size[0] + 100

        if self.last_obstacle_type == ObstacleType.LOW:
            weights: list[float] = [0.3, 0.7]
        elif self.last_obstacle_type == ObstacleType.HIGH:
            weights: list[float] = [0.7, 0.3]
        else:
            weights = [0.5, 0.5]

        obstacle_type: ObstacleType = random.choices(
            [ObstacleType.LOW, ObstacleType.HIGH],
            weights=weights
        )[0]

        self.last_obstacle_type = obstacle_type

        obstacle: Obstacle = Obstacle(x, self.ground_y, obstacle_type)
        obstacle.speed = self.scroll_speed
        self.obstacles.add(obstacle)

    def _check_collision(self, obstacle: Obstacle) -> bool:
        player_state: PlayerState = self.player.state
        obstacle_type: ObstacleType = obstacle.obstacle_type
        player_hitbox: pygame.Rect = self.player.get_hitbox()
        obstacle_hitbox: pygame.Rect = obstacle.get_hitbox()

        if not player_hitbox.colliderect(obstacle_hitbox):
            return False

        if obstacle_type == ObstacleType.LOW and player_state == PlayerState.JUMPING:
            if player_hitbox.bottom < obstacle_hitbox.top + 20:
                return False

        if obstacle_type == ObstacleType.HIGH and player_state == PlayerState.SLIDING:
            if player_hitbox.top > obstacle_hitbox.bottom - 15:
                return False

        return True

    def _check_collisions(self) -> None:
        if self.invincible_timer > 0:
            return

        for obstacle in list(self.obstacles):
            if self._check_collision(obstacle):
                self.invincible_timer = self.invincible_duration
                self.chaser.on_player_hit()
                obstacle.kill()
                break

        if self.chaser.has_caught_player(self.player.get_hitbox()):
            self.game_over = True

    def update(self, dt: float) -> None:
        if self.game_over:
            return

        self.scroll_x += self.scroll_speed * dt
        if self.scroll_x >= self.bg_width:
            self.scroll_x -= self.bg_width

        self.score += int(self.scroll_speed * dt * 0.1)

        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        self.player.update(dt)

        self.chaser.set_target(self.player.rect.centerx, self.player.rect.centery)
        self.chaser.update(dt)

        self.obstacle_timer += dt
        if self.obstacle_timer >= self.obstacle_spawn_delay:
            self._spawn_obstacle()
            self.obstacle_timer = 0.0
            self.obstacle_spawn_delay = random.uniform(
                self.OBSTACLE_MIN_DELAY,
                self.OBSTACLE_MAX_DELAY
            )

        for obstacle in list(self.obstacles):
            obstacle.update(dt)
            if obstacle.is_off_screen():
                obstacle.kill()

        self._check_collisions()

    def _draw_ground(self, screen: Surface) -> None:
        ground_color: tuple[int, int, int] = (139, 119, 101)
        ground_rect: pygame.Rect = pygame.Rect(
            0, self.ground_y,
            self.screen_size[0], self.screen_size[1] - self.ground_y
        )
        pygame.draw.rect(screen, ground_color, ground_rect)

        line_color: tuple[int, int, int] = (119, 99, 81)
        pygame.draw.line(
            screen, line_color,
            (0, self.ground_y), (self.screen_size[0], self.ground_y), 3
        )

    def draw(self, screen: Surface) -> None:
        x1: int = -int(self.scroll_x)
        x2: int = x1 + self.bg_width

        screen.blit(self.background, (x1, 0))
        screen.blit(self.background, (x2, 0))

        self._draw_ground(screen)

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
        score_text: str = f"Score: {self.score}"
        text_surface: Surface = self.score_font.render(score_text, True, WHITE)
        shadow_surface: Surface = self.score_font.render(score_text, True, (0, 0, 0))
        screen.blit(shadow_surface, (22, 22))
        screen.blit(text_surface, (20, 20))

        controls_text: str = "ESPACE: Sauter | BAS: Glisser"
        controls_surface: Surface = self.small_font.render(controls_text, True, WHITE)
        controls_shadow: Surface = self.small_font.render(controls_text, True, (0, 0, 0))
        screen.blit(controls_shadow, (22, self.screen_size[1] - 38))
        screen.blit(controls_surface, (20, self.screen_size[1] - 40))

    def _draw_game_over(self, screen: Surface) -> None:
        overlay: Surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        text: Surface = self.font.render(GAME_OVER, True, (255, 50, 50))
        text_rect = text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 - 50))
        screen.blit(text, text_rect)

        score_final: str = f"Score Final: {self.score}"
        score_surface: Surface = self.score_font.render(score_final, True, GOLD)
        score_rect = score_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + 10))
        screen.blit(score_surface, score_rect)

        restart_text: Surface = self.small_font.render(GAME_RESTART, True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + 60))
        screen.blit(restart_text, restart_rect)
