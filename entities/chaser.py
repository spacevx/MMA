import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from settings import Color, ScreenSize


class Chaser(Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.width: int = 45
        self.height: int = 65
        self.speed: float = 180.0

        self.image: Surface = self._create_image()
        self.rect: Rect = self.image.get_rect(center=(x, y))

        self.target_x: int = x
        self.target_y: int = y
        self.screen_size: ScreenSize = (800, 600)
        self.ground_y: int = 500

    def _create_image(self) -> Surface:
        surface: Surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        skin_color: Color = (180, 140, 100)
        shorts_color: Color = (30, 30, 30)

        pygame.draw.circle(surface, skin_color, (self.width // 2, 14), 12)
        pygame.draw.rect(surface, skin_color, (self.width // 2 - 10, 24, 20, 28))
        pygame.draw.rect(surface, shorts_color, (self.width // 2 - 12, 46, 24, 14))
        pygame.draw.rect(surface, skin_color, (self.width // 2 - 10, 60, 8, 5))
        pygame.draw.rect(surface, skin_color, (self.width // 2 + 2, 60, 8, 5))
        pygame.draw.rect(surface, skin_color, (self.width // 2 - 18, 26, 8, 6))
        pygame.draw.rect(surface, skin_color, (self.width // 2 + 10, 26, 8, 6))

        return surface

    def set_screen_size(self, size: ScreenSize) -> None:
        self.screen_size = size
        self.ground_y = int(size[1] * 0.85)

    def set_target(self, x: int, y: int) -> None:
        self.target_x = x
        self.target_y = y

    def update(self, dt: float) -> None:
        dx: float = self.target_x - self.rect.centerx
        dy: float = self.target_y - self.rect.centery

        distance: float = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 5:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed

            self.rect.x += int(dx * dt)
            self.rect.y += int(dy * dt)

        margin: int = 0
        self.rect.left = max(margin, self.rect.left)
        self.rect.right = min(self.screen_size[0] - margin, self.rect.right)
        self.rect.top = max(self.ground_y - 100, self.rect.top)
        self.rect.bottom = min(self.ground_y, self.rect.bottom)
