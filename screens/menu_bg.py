# Background of the start menu

from __future__ import annotations

import math
from pathlib import Path

import pygame
from pygame import Surface

from settings import ScreenSize
from entities import (
    Player,
    TileSet, GroundTilemap, CeilingTileSet, CeilingTilemap, Ceiling
)
from paths import assetsPath, screensPath

tilesPath = assetsPath / "tiles" / "ground"
ceilingTilesPath = assetsPath / "tiles" / "ceiling"


class MenuBackground:
    baseW: int = 1280
    baseH: int = 720
    scrollSpeed: float = 300.0
    groundRatio: float = 1.0
    ceilingRatio: float = 0.0542
    overlayAlpha: int = 130

    def __init__(self, screenSize: ScreenSize, backgroundPath: Path | None = None,
                 bHasCeilingTiles: bool = True) -> None:
        self.screenSize = screenSize
        self.scale = min(screenSize[0] / self.baseW, screenSize[1] / self.baseH)
        self.groundY = int(screenSize[1] * self.groundRatio)
        self.scrollX: float = 0.0
        self.backgroundPath = backgroundPath
        self.bHasCeilingTiles = bHasCeilingTiles # Only the first map have tiles, so we have to disable it for others maps (else it's going to render tiles from the first map)
        self._loadBackground()
        self._initTilemap()
        if self.bHasCeilingTiles:
            self._initCeilingTilemap()

        self.demoPlayer = Player(self._s(320), self.groundY)

        self._buildOverlay()

    # Scaling function, converts base resolution values to our current screen res
    def _s(self, val: int) -> int:
        return max(1, int(val * self.scale))

    def _loadBackground(self) -> None:
        path = self.backgroundPath or screensPath / "background.png"
        original = pygame.image.load(str(path)).convert()
        self.background = pygame.transform.scale(original, self.screenSize)
        self.bgWidth = self.background.get_width()

    def _initTilemap(self) -> None:
        w = self.screenSize[0]
        groundH = self.screenSize[1] - self.groundY
        self.tileset = TileSet(tilesPath)
        self.groundTilemap = GroundTilemap(self.tileset, w, self.groundY, groundH)

    def _initCeilingTilemap(self) -> None:
        w = self.screenSize[0]
        self.ceilingY = int(self.screenSize[1] * self.ceilingRatio)
        self.ceiling = Ceiling(w, self.screenSize[1], self.ceilingY)
        self.ceilingTileset = CeilingTileSet(ceilingTilesPath)
        self.ceilingTilemap = CeilingTilemap(self.ceilingTileset, w, self.ceiling.height)

    def _buildOverlay(self) -> None:
        w, h = self.screenSize
        self.overlaySurf = Surface((w, h), pygame.SRCALPHA)
        self.overlaySurf.fill((0, 0, 0, self.overlayAlpha))
        cx, cy = w // 2, h // 2
        maxDist = math.hypot(cx, cy)  # diagonal distance center -> corner
        for ring in range(0, int(maxDist), 6):
            t = ring / maxDist
            alpha = int(60 * (t ** 2.5))
            if alpha > 0:
                pygame.draw.circle(self.overlaySurf, (0, 0, 0, alpha), (cx, cy), int(maxDist - ring), 6)

    def update(self, dt: float) -> None:
        scrollDelta = self.scrollSpeed * dt
        self.scrollX += scrollDelta
        if self.scrollX >= self.bgWidth:
            self.scrollX -= self.bgWidth

        self.groundTilemap.update(scrollDelta)
        if self.bHasCeilingTiles:
            self.ceilingTilemap.update(scrollDelta)

        self.demoPlayer.update(dt)

    def draw(self, screen: Surface) -> None:
        x1 = -int(self.scrollX)
        x2 = x1 + self.bgWidth
        screen.blit(self.background, (x1, 0))
        screen.blit(self.background, (x2, 0))

        # Same logic as in game for scrolling the background

        self.groundTilemap.draw(screen)
        screen.blit(self.demoPlayer.image, self.demoPlayer.rect)
        if self.bHasCeilingTiles:
            self.ceilingTilemap.draw(screen)

        screen.blit(self.overlaySurf, (0, 0))

    # Won't work well have to do more tests
    def onResize(self, newSize: ScreenSize) -> None:
        self.screenSize = newSize
        self.scale = min(newSize[0] / self.baseW, newSize[1] / self.baseH)
        self.groundY = int(newSize[1] * self.groundRatio)
        self.ceilingY = int(newSize[1] * self.ceilingRatio)

        self._loadBackground()
        self.groundTilemap.on_resize(newSize[0], self.groundY, newSize[1] - self.groundY)
        if self.bHasCeilingTiles:
            self.ceiling.onResize(newSize[0], self.ceilingY)
            self.ceilingTilemap.on_resize(newSize[0], self.ceiling.height)
        self.demoPlayer.setGroundY(self.groundY)
        self._buildOverlay()
