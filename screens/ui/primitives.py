from __future__ import annotations

import sys
import pygame
from pygame import Surface
from pygame.font import Font
from typing import Any

_BROWSER: bool = sys.platform == "emscripten"

if _BROWSER:
    from enum import Enum

    class OutlineIcon(Enum):
        CHEVRON_LEFT = "chevron_left"
        CHEVRON_RIGHT = "chevron_right"
        LOCK = "lock"
        PLAYER_PLAY = "player_play"

    class FilledIcon(Enum):
        HEART = "heart"
        CIRCLE_CHECK = "circle_check"

    _TablerIcons: Any = None
else:
    from pytablericons import TablerIcons as _TablerIcons, OutlineIcon, FilledIcon  # type: ignore[import-untyped,no-redef]

_iconCache: dict[tuple[Any, ...], Surface] = {}


def tablerIcon(icon: OutlineIcon | FilledIcon, size: int = 32, color: str = '#FFFFFF', strokeWidth: float = 2.0) -> Surface:
    key = (icon, size, color, strokeWidth)
    if key in _iconCache:
        return _iconCache[key]

    if _BROWSER:
        surf = Surface((size, size), pygame.SRCALPHA)
        r, g, b = _parseColor(color)
        pygame.draw.circle(surf, (r, g, b), (size // 2, size // 2), size // 3)
        _iconCache[key] = surf
        return surf

    pil = _TablerIcons.load(icon, size=size, color=color, stroke_width=strokeWidth)
    surf = pygame.image.frombuffer(pil.tobytes(), pil.size, pil.mode)
    if pil.mode == 'RGBA':
        surf = surf.convert_alpha()
    _iconCache[key] = surf
    return surf


def _parseColor(color: str) -> tuple[int, int, int]:
    c = color.lstrip('#')
    if len(c) == 6:
        return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (255, 255, 255)


def _gradientRect(w: int, h: int, top: tuple[int, int, int], bot: tuple[int, int, int], alpha: int, cr: int) -> Surface:
    surf = Surface((w, h), pygame.SRCALPHA)
    if w < 1 or h < 1:
        return surf
    grad = Surface((1, 2), pygame.SRCALPHA)
    grad.set_at((0, 0), (*top, alpha))
    grad.set_at((0, 1), (*bot, alpha))
    stretched = pygame.transform.smoothscale(grad, (w, h))
    mask = Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=cr)
    stretched.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(stretched, (0, 0))
    return surf


def drawTextWithShadow(target: Surface, text: str, font: Font,
                       color: tuple[int, int, int], pos: tuple[int, int],
                       shadowOffset: int = 2) -> None:
    shadow = font.render(text, True, (0, 0, 0))
    surf = font.render(text, True, color)
    target.blit(shadow, (pos[0] + shadowOffset, pos[1] + shadowOffset))
    target.blit(surf, pos)


def glassPanel(w: int, h: int, scale: float) -> Surface:
    cr = max(1, int(12 * scale))
    panel = _gradientRect(w, h, (20, 22, 30), (12, 14, 20), 200, cr)
    pygame.draw.rect(panel, (45, 48, 60), (0, 0, w, h), 1, border_radius=cr)
    return panel
