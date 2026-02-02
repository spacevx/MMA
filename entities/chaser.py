import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from settings import Color, ScreenSize


class Chaser(Sprite):
    BASE_SPEED: float = 150.0
    SPEED_BOOST_ON_HIT: float = 50.0
    APPROACH_ON_HIT: int = 80

    def __init__(self, x: int, ground_y: int) -> None:
        super().__init__()
        self.width: int = 140
        self.height: int = 95

        self.image: Surface = self._create_image()
        self.rect: Rect = self.image.get_rect()

        self.screen_size: ScreenSize = (800, 600)
        self.ground_y: int = ground_y
        self.base_offset: float = float(x)
        self.speed: float = self.BASE_SPEED

        self.rect.midbottom = (int(self.base_offset), ground_y)

        self.target_x: int = x
        self.player_x: int = 100

    def _create_image(self) -> Surface:
        surface: Surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        body_color: Color = (80, 50, 30)
        horn_color: Color = (200, 180, 150)

        pygame.draw.ellipse(surface, body_color, (10, 25, 110, 55))
        pygame.draw.circle(surface, body_color, (110, 45), 28)
        pygame.draw.polygon(surface, horn_color, [(120, 25), (140, 8), (130, 30)])
        pygame.draw.polygon(surface, horn_color, [(120, 65), (140, 82), (130, 60)])
        pygame.draw.circle(surface, (0, 0, 0), (124, 40), 5)
        pygame.draw.circle(surface, (255, 0, 0), (124, 40), 3)
        pygame.draw.rect(surface, body_color, (16, 75, 12, 20))
        pygame.draw.rect(surface, body_color, (40, 75, 12, 20))
        pygame.draw.rect(surface, body_color, (70, 75, 12, 20))
        pygame.draw.rect(surface, body_color, (94, 75, 12, 20))
        pygame.draw.ellipse(surface, body_color, (0, 35, 25, 15))

        return surface

    def set_screen_size(self, size: ScreenSize) -> None:
        self.screen_size = size

    def set_ground_y(self, ground_y: int) -> None:
        self.ground_y = ground_y
        self.rect.bottom = ground_y

    def set_target(self, player_x: int, player_y: int) -> None:
        self.player_x = player_x
        self.target_x = player_x - 150

    def on_player_hit(self) -> None:
        self.speed += self.SPEED_BOOST_ON_HIT
        self.base_offset += self.APPROACH_ON_HIT

    def reset(self, start_x: int) -> None:
        self.base_offset = float(start_x)
        self.speed = self.BASE_SPEED
        self.rect.midbottom = (int(self.base_offset), self.ground_y)

    def has_caught_player(self, player_rect: Rect) -> bool:
        return self.rect.colliderect(player_rect)

    def update(self, dt: float) -> None:
        target: float = float(self.target_x)
        diff: float = target - self.base_offset

        if diff > 0:
            move: float = min(self.speed * dt, diff)
            self.base_offset += move
        elif diff < 0:
            move = min(self.speed * 0.5 * dt, -diff)
            self.base_offset -= move

        max_x: float = float(self.player_x - 50)
        if self.base_offset > max_x:
            self.base_offset = max_x

        self.rect.midbottom = (int(self.base_offset), self.ground_y)
