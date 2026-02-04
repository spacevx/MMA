from pathlib import Path

import pygame
from pygame import Surface, Rect

from settings import Color
from paths import assetsPath
from entities.animation import loadFrames
from entities.player import getRunningHeight
from .base import BaseObstacle

playerRunningFramesPath = assetsPath / "player" / "running" / "frames"


class Obstacle(BaseObstacle):
    _texture: Surface | None = None
    _cache: dict[tuple[int, int], Surface] = {}
    _playerHeight: int | None = None

    bodyImagePath: Path = assetsPath / "lanes" / "body.png"
    playerScale: float = 0.15
    heightRatio: float = 2.0
    widthRatio: float = 1.8

    @classmethod
    def _getPlayerHeight(cls) -> int:
        if cls._playerHeight is None:
            cls._playerHeight = getRunningHeight(cls.playerScale)
        return cls._playerHeight

    def __init__(self, x: int, groundY: int, scale: float = 1.0) -> None:
        super().__init__()
        self.scale = scale
        playerH = self._getPlayerHeight()
        h = max(1, int(playerH * self.heightRatio * scale))
        w = max(1, int(h * self.widthRatio))
        self.image = self._getImage(w, h)
        self.rect = self.image.get_rect(centerx=x, bottom=groundY)

    @classmethod
    def clearCache(cls) -> None:
        cls._texture = None
        cls._cache.clear()
        cls._playerHeight = None

    @classmethod
    def _loadTexture(cls) -> Surface | None:
        if cls._texture is None:
            try:
                raw = pygame.image.load(str(cls.bodyImagePath))
                if pygame.display.get_surface():
                    cls._texture = raw.convert_alpha()
                else:
                    cls._texture = raw
            except (pygame.error, FileNotFoundError):
                cls._texture = None
        return cls._texture

    @classmethod
    def _getImage(cls, w: int, h: int) -> Surface:
        key = (w, h)
        if key not in cls._cache:
            cls._cache[key] = cls._createSurface(w, h)
        return cls._cache[key]

    @classmethod
    def _createSurface(cls, w: int, h: int) -> Surface:
        if (texture := cls._loadTexture()) is not None:
            tw, th = texture.get_width(), texture.get_height()
            srcRatio = tw / th
            tgtRatio = w / h

            if srcRatio > tgtRatio:
                sw = w
                sh = max(1, int(w / srcRatio))
            else:
                sh = h
                sw = max(1, int(h * srcRatio))

            scaled = pygame.transform.smoothscale(texture, (sw, sh))
            surface = pygame.Surface((sw, sh), pygame.SRCALPHA)
            surface.blit(scaled, (0, 0))
            return surface
        else:
            return cls._createFallback(w, h)

    @classmethod
    def _createFallback(cls, w: int, h: int) -> Surface:
        surface = pygame.Surface((w, h), pygame.SRCALPHA)

        bodyColor: Color = (80, 40, 40)
        darkColor: Color = (50, 25, 25)
        outlineColor: Color = (30, 15, 15)

        pygame.draw.ellipse(surface, bodyColor, (0, 0, w, h))
        pygame.draw.ellipse(surface, darkColor, (0, 0, w, h), 3)

        headRadius = h // 2
        headX = w - headRadius - 5
        headY = h // 2
        pygame.draw.circle(surface, bodyColor, (headX, headY), headRadius)
        pygame.draw.circle(surface, outlineColor, (headX, headY), headRadius, 2)

        armW, armH = w // 4, h // 5
        pygame.draw.ellipse(surface, darkColor, (10, h // 2 - armH // 2, armW, armH))

        return surface

    def get_hitbox(self) -> Rect:
        shrinkX = int(self.rect.width * 0.15)
        shrinkY = int(self.rect.height * 0.1)
        return self.rect.inflate(-shrinkX, -shrinkY)
