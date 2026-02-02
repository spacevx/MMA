import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from settings import Color, ScreenSize


class Player(Sprite):
    def __init__(self, x: int, lane_y: int) -> None:
        super().__init__()
        self.width: int = 40
        self.height: int = 50
        self.speed: float = 400.0

        self.image: Surface = self._create_image()
        self.rect: Rect = self.image.get_rect(center=(x, lane_y))

        self.screen_size: ScreenSize = (800, 600)
        self.base_x: int = x

        self.lanes: list[int] = []
        self.current_lane: int = 1
        self.target_y: float = float(lane_y)

    def _create_image(self) -> Surface:
        surface: Surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        skin_color: Color = (210, 180, 140)
        shorts_color: Color = (200, 30, 30)

        pygame.draw.circle(surface, skin_color, (self.width // 2, 10), 8)
        pygame.draw.rect(surface, skin_color, (self.width // 2 - 7, 17, 14, 20))
        pygame.draw.rect(surface, shorts_color, (self.width // 2 - 9, 34, 18, 10))
        pygame.draw.rect(surface, skin_color, (self.width // 2 - 7, 44, 5, 6))
        pygame.draw.rect(surface, skin_color, (self.width // 2 + 2, 44, 5, 6))
        pygame.draw.rect(surface, skin_color, (self.width // 2 - 14, 19, 7, 4))
        pygame.draw.rect(surface, skin_color, (self.width // 2 + 7, 19, 7, 4))

        return surface

    def set_lanes(self, lanes: list[int]) -> None:
        self.lanes = lanes
        if self.lanes:
            self.current_lane = len(lanes) // 2
            self.target_y = float(lanes[self.current_lane])
            self.rect.centery = int(self.target_y)

    def set_screen_size(self, size: ScreenSize) -> None:
        self.screen_size = size

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_z):
                if self.current_lane > 0:
                    self.current_lane -= 1
                    self.target_y = float(self.lanes[self.current_lane])
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if self.current_lane < len(self.lanes) - 1:
                    self.current_lane += 1
                    self.target_y = float(self.lanes[self.current_lane])

    def update(self, dt: float) -> None:
        diff: float = self.target_y - self.rect.centery
        if abs(diff) > 2:
            self.rect.centery += int(diff * 10 * dt)
        else:
            self.rect.centery = int(self.target_y)

        self.rect.centerx = self.base_x
