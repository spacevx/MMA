from enum import Enum, auto
import math

import pygame
from pygame import Surface
from pygame.math import Vector2


class SlideDir(Enum):
    LEFT = auto()
    RIGHT = auto()


class FadePhase(Enum):
    OUT = auto()
    IN = auto()


def _easeOutCubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def _easeInOutSine(t: float) -> float:
    return 0.5 * (1.0 - math.cos(math.pi * t))


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


class FadeTransition:
    fadeOutDuration: float = 0.35
    fadeInDuration: float = 0.35

    def __init__(self, screenSize: tuple[int, int]) -> None:
        self.screenSize = screenSize
        self.bActive: bool = False
        self.phase: FadePhase = FadePhase.OUT
        self.elapsed: float = 0.0
        self.alpha: int = 0
        self.bMidpointFired: bool = False

        self._overlay: Surface = Surface(screenSize)
        self._overlay.fill((0, 0, 0))

    def start(self) -> None:
        self.bActive = True
        self.phase = FadePhase.OUT
        self.elapsed = 0.0
        self.alpha = 0
        self.bMidpointFired = False

    def update(self, dt: float) -> bool:
        if not self.bActive:
            return False

        self.elapsed += dt

        if self.phase == FadePhase.OUT:
            t = min(self.elapsed / self.fadeOutDuration, 1.0)
            self.alpha = int(_easeInOutSine(t) * 255)
            if t >= 1.0:
                self.alpha = 255
                self.bMidpointFired = True
                self.phase = FadePhase.IN
                self.elapsed = 0.0
        else:
            t = min(self.elapsed / self.fadeInDuration, 1.0)
            self.alpha = int((1.0 - _easeInOutSine(t)) * 255)
            if t >= 1.0:
                self.alpha = 0
                self.bActive = False
                return True

        return False

    def draw(self, screen: Surface) -> None:
        if not self.bActive:
            return
        self._overlay.set_alpha(self.alpha)
        screen.blit(self._overlay, (0, 0))

    def onResize(self, newSize: tuple[int, int]) -> None:
        self.screenSize = newSize
        self._overlay = Surface(newSize)
        self._overlay.fill((0, 0, 0))
        self.bActive = False
