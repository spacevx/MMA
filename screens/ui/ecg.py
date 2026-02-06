from __future__ import annotations

import math

import pygame
from pygame import Surface


class EcgMonitor:
    sweepSpeed: float = 1.5
    cyclePeriod: float = 0.8

    def __init__(self, scale: float) -> None:
        self.scale = scale
        self._startTick: int = 0

    def _s(self, val: int) -> int:
        return max(1, int(val * self.scale))

    def reset(self) -> None:
        self._startTick = pygame.time.get_ticks()

    def onResize(self, scale: float) -> None:
        self.scale = scale

    @staticmethod
    def _sample(t: float) -> float:
        t = t % 1.0
        if t < 0.10:
            return 0.15 * math.sin(math.pi * t / 0.10)
        if t < 0.16:
            return 0.0
        if t < 0.20:
            return -0.15 * math.sin(math.pi * (t - 0.16) / 0.04)
        if t < 0.26:
            return 1.0 * math.sin(math.pi * (t - 0.20) / 0.06)
        if t < 0.30:
            return -0.3 * math.sin(math.pi * (t - 0.26) / 0.04)
        if t < 0.44:
            return 0.2 * math.sin(math.pi * (t - 0.30) / 0.14)
        return 0.0

    def draw(self, screen: Surface, x: int, y: int, w: int, h: int) -> None:
        elapsed = (pygame.time.get_ticks() - self._startTick) / 1000.0
        cursorFrac = (elapsed % self.sweepSpeed) / self.sweepSpeed

        midY = y + h // 2
        amplitude = h * 0.45
        stepCount = max(2, w)

        points: list[tuple[int, int]] = []
        for i in range(stepCount):
            frac = i / (stepCount - 1)
            worldTime = elapsed - (cursorFrac - frac) * self.sweepSpeed
            sample = self._sample(worldTime / self.cyclePeriod)
            px = x + int(frac * w)
            py = int(midY - sample * amplitude)
            points.append((px, py))

        gapStart = max(0, int(cursorFrac * stepCount))
        gapEnd = min(stepCount, gapStart + max(1, stepCount // 12))

        before = points[:gapStart]
        after = points[gapEnd:]

        for segment in (before, after):
            if len(segment) >= 2:
                glowSurf = pygame.Surface((w + self._s(10), h + self._s(10)), pygame.SRCALPHA)
                ox, oy = x - self._s(5), y - self._s(5)
                shifted = [(px - ox, py - oy) for px, py in segment]
                pygame.draw.lines(glowSurf, (200, 20, 20, 80), False, shifted, max(1, self._s(4)))
                screen.blit(glowSurf, (ox, oy))
                pygame.draw.aalines(screen, (255, 40, 40), False, segment)

        tipX = x + int(cursorFrac * w)
        tipY = points[min(gapStart, stepCount - 1)][1]
        pygame.draw.circle(screen, (255, 100, 100), (tipX, tipY), self._s(4))
        pygame.draw.circle(screen, (255, 200, 200), (tipX, tipY), self._s(2))
