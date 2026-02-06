from enum import Enum, auto

import pygame
from pygame import Surface
from pygame.math import Vector2


class SlideDir(Enum):
    LEFT = auto()
    RIGHT = auto()


def _easeOutCubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


class ScreenTransition:
    duration: float = 0.4

    def __init__(self, screenSize: tuple[int, int]) -> None:
        self.screenSize = screenSize
        self.bActive: bool = False
        self.elapsed: float = 0.0
        self.direction: SlideDir = SlideDir.LEFT

        w, h = screenSize
        self.fromSurf: Surface = Surface((w, h))
        self.toSurf: Surface = Surface((w, h))
        self.fromPos: Vector2 = Vector2(0, 0)
        self.toPos: Vector2 = Vector2(0, 0)
        self._onComplete: type[None] | None = None

    def start(self, fromSurf: Surface, toSurf: Surface, direction: SlideDir) -> None:
        self.bActive = True
        self.elapsed = 0.0
        self.direction = direction

        w, h = self.screenSize
        if self.fromSurf.get_size() != (w, h):
            self.fromSurf = Surface((w, h))
            self.toSurf = Surface((w, h))

        self.fromSurf.blit(fromSurf, (0, 0))
        self.toSurf.blit(toSurf, (0, 0))

        self.fromPos = Vector2(0, 0)
        if direction == SlideDir.LEFT:
            self.toPos = Vector2(w, 0)
        else:
            self.toPos = Vector2(-w, 0)

    def update(self, dt: float) -> bool:
        if not self.bActive:
            return False

        self.elapsed += dt
        t = min(self.elapsed / self.duration, 1.0)
        eased = _easeOutCubic(t)

        w = self.screenSize[0]
        if self.direction == SlideDir.LEFT:
            self.fromPos.x = pygame.math.lerp(0.0, float(-w), eased)
            self.toPos.x = pygame.math.lerp(float(w), 0.0, eased)
        else:
            self.fromPos.x = pygame.math.lerp(0.0, float(w), eased)
            self.toPos.x = pygame.math.lerp(float(-w), 0.0, eased)

        if t >= 1.0:
            self.bActive = False
            return True

        return False

    def draw(self, screen: Surface) -> None:
        if not self.bActive:
            return
        screen.blit(self.fromSurf, (int(self.fromPos.x), int(self.fromPos.y)))
        screen.blit(self.toSurf, (int(self.toPos.x), int(self.toPos.y)))

    def onResize(self, newSize: tuple[int, int]) -> None:
        self.screenSize = newSize
        self.bActive = False
