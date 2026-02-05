import math
from typing import Callable, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.font import Font

if TYPE_CHECKING:
    from entities.input.manager import InputEvent

from settings import GameState, ScreenSize
from keybindings import keyBindings
from strings import (
    optionsTitle, optionsControls, optionsJump, optionsSlide, optionsRestart,
    optionsReset, optionsBack, optionsPressKey
)
from screens.menu_bg import MenuBackground
from screens.ui import ModernButton


class OptionsScreen:
    baseW: int = 1920
    baseH: int = 1080

    def __init__(self, screenSize: ScreenSize, setStateCallback: Callable[[GameState], None]) -> None:
        self.setState: Callable[[GameState], None] = setStateCallback
        self.screenSize: ScreenSize = screenSize
        self.scale: float = min(screenSize[0] / self.baseW, screenSize[1] / self.baseH)

        self.menuBg = MenuBackground(screenSize)

        self.panelSurf: Surface | None = None

        self.buttonFont: Font = pygame.font.Font(None, self._s(28))
        self.labelFont: Font = pygame.font.Font(None, self._s(32))

        self.iconSize: int = self._s(50)
        self.jumpIcon: Surface | None = None
        self.slideIcon: Surface | None = None
        self.restartIcon: Surface | None = None
        self.jumpIconRect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.slideIconRect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.restartIconRect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.bJumpHovered: bool = False
        self.bSlideHovered: bool = False
        self.bRestartHovered: bool = False

        self.resetBtn: ModernButton
        self.backBtn: ModernButton

        self._loadKeyIcons()
        self._updateIconRects()
        self._createActionButtons()

        self.titleFont: Font = pygame.font.Font(None, self._s(120))
        self.sectionFont: Font = pygame.font.Font(None, self._s(48))

        self.time: float = 0.0
        self.titlePulse: float = 0.0

        self.bListeningJump: bool = False
        self.bListeningSlide: bool = False
        self.bListeningRestart: bool = False

    def _s(self, val: int) -> int:
        return max(1, int(val * self.scale))

    def _getKeyIconRects(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        w, h = self.screenSize
        cx = w // 2
        baseY = int(h * 0.42)
        gap = self._s(70)
        sz = self.iconSize
        labelOffset = self._s(120)

        jumpRect = pygame.Rect(cx + labelOffset - sz // 2, baseY + self._s(25) - sz // 2, sz, sz)
        slideRect = pygame.Rect(cx + labelOffset - sz // 2, baseY + gap + self._s(25) - sz // 2, sz, sz)
        restartRect = pygame.Rect(cx + labelOffset - sz // 2, baseY + gap * 2 + self._s(25) - sz // 2, sz, sz)
        return jumpRect, slideRect, restartRect

    def _getActionButtonRects(self) -> tuple[pygame.Rect, pygame.Rect]:
        w, h = self.screenSize
        cx = w // 2
        baseY = int(h * 0.75)
        btnW, btnH = self._s(220), self._s(55)
        gap = self._s(40)

        resetRect = pygame.Rect(cx - btnW - gap // 2, baseY, btnW, btnH)
        backRect = pygame.Rect(cx + gap // 2, baseY, btnW, btnH)
        return resetRect, backRect

    def _loadKeyIcons(self) -> None:
        self.jumpIcon = keyBindings.getKeyIcon(keyBindings.jump, self.iconSize)
        self.slideIcon = keyBindings.getKeyIcon(keyBindings.slide, self.iconSize)
        self.restartIcon = keyBindings.getKeyIcon(keyBindings.restart, self.iconSize)

    def _updateIconRects(self) -> None:
        self.jumpIconRect, self.slideIconRect, self.restartIconRect = self._getKeyIconRects()

    def _createActionButtons(self) -> None:
        resetRect, backRect = self._getActionButtonRects()
        self.resetBtn = ModernButton(resetRect, optionsReset, self.buttonFont)
        self.backBtn = ModernButton(backRect, optionsBack, self.buttonFont)

    def _updateKeyIcons(self) -> None:
        self._loadKeyIcons()

    def _updateButtonPositions(self) -> None:
        self._updateIconRects()
        resetRect, backRect = self._getActionButtonRects()

        for btn, rect in [(self.resetBtn, resetRect), (self.backBtn, backRect)]:
            btn.setPosition(rect.x, rect.y)
            btn.setDimensions(rect.width, rect.height)

    def _buildPanelSurf(self) -> None:
        panelW, panelH = self._s(600), self._s(340)
        surf = pygame.Surface((panelW, panelH), pygame.SRCALPHA)
        cr = self._s(12)
        pygame.draw.rect(surf, (15, 17, 24, 200), (0, 0, panelW, panelH), border_radius=cr)
        pygame.draw.rect(surf, (45, 48, 60), (0, 0, panelW, panelH), 1, border_radius=cr)
        self.panelSurf = surf

    def _drawTitle(self, surf: Surface) -> None:
        w, h = self.screenSize
        cx, ty = w // 2, int(h * 0.15)
        text = optionsTitle
        pulse = 0.9 + 0.1 * math.sin(self.titlePulse)

        for offset in range(self._s(15), 0, -2):
            alpha = int(60 * (1 - offset / self._s(15)) * pulse)
            glowSurf = self.titleFont.render(text, True, (139, 0, 0))
            glowSurf.set_alpha(alpha)
            for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset)]:
                rect = glowSurf.get_rect(center=(cx + dx, ty + dy))
                surf.blit(glowSurf, rect)

        shadow = self.titleFont.render(text, True, (20, 0, 0))
        shadowRect = shadow.get_rect(center=(cx + self._s(4), ty + self._s(4)))
        surf.blit(shadow, shadowRect)

        titleSurf = self.titleFont.render(text, True, (220, 220, 230))
        titleRect = titleSurf.get_rect(center=(cx, ty))
        surf.blit(titleSurf, titleRect)

    def _drawControlsPanel(self, surf: Surface) -> None:
        w, h = self.screenSize
        cx = w // 2

        if self.panelSurf is None:
            self._buildPanelSurf()

        assert self.panelSurf is not None
        panelW, panelH = self.panelSurf.get_size()
        panelX = cx - panelW // 2
        panelY = int(h * 0.35)
        surf.blit(self.panelSurf, (panelX, panelY))

        sectionY = int(h * 0.38)
        glowSurf = self.sectionFont.render(optionsControls, True, (255, 215, 0))
        glowSurf.set_alpha(40)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            rect = glowSurf.get_rect(center=(cx + dx, sectionY + dy))
            surf.blit(glowSurf, rect)
        sectionSurf = self.sectionFont.render(optionsControls, True, (255, 215, 0))
        sectionRect = sectionSurf.get_rect(center=(cx, sectionY))
        surf.blit(sectionSurf, sectionRect)

        baseY = int(h * 0.42)
        gap = self._s(70)
        labelX = cx - self._s(120)

        jumpLabelSurf = self.labelFont.render(optionsJump, True, (240, 240, 245))
        jumpLabelRect = jumpLabelSurf.get_rect(midright=(labelX, baseY + self._s(25)))
        surf.blit(jumpLabelSurf, jumpLabelRect)

        slideLabelSurf = self.labelFont.render(optionsSlide, True, (240, 240, 245))
        slideLabelRect = slideLabelSurf.get_rect(midright=(labelX, baseY + gap + self._s(25)))
        surf.blit(slideLabelSurf, slideLabelRect)

        restartLabelSurf = self.labelFont.render(optionsRestart, True, (240, 240, 245))
        restartLabelRect = restartLabelSurf.get_rect(midright=(labelX, baseY + gap * 2 + self._s(25)))
        surf.blit(restartLabelSurf, restartLabelRect)

        self._drawKeyIcon(surf, self.jumpIcon, self.jumpIconRect,
                          self.bListeningJump, self.bJumpHovered,
                          keyBindings.getKeyName(keyBindings.jump))
        self._drawKeyIcon(surf, self.slideIcon, self.slideIconRect,
                          self.bListeningSlide, self.bSlideHovered,
                          keyBindings.getKeyName(keyBindings.slide))
        self._drawKeyIcon(surf, self.restartIcon, self.restartIconRect,
                          self.bListeningRestart, self.bRestartHovered,
                          keyBindings.getKeyName(keyBindings.restart))

    def _drawKeyIcon(self, surf: Surface, icon: Surface | None, rect: pygame.Rect,
                      bListening: bool, bHovered: bool, fallbackText: str) -> None:
        pad = self._s(4)
        if bHovered or bListening:
            highlight = pygame.Surface((rect.width + pad * 2, rect.height + pad * 2), pygame.SRCALPHA)
            cr = self._s(6)
            color = (255, 215, 0, 50) if bListening else (255, 255, 255, 30)
            pygame.draw.rect(highlight, color, highlight.get_rect(), border_radius=cr)
            surf.blit(highlight, (rect.x - pad, rect.y - pad))

        if bListening:
            listenSurf = self.buttonFont.render(optionsPressKey, True, (255, 215, 0))
            listenRect = listenSurf.get_rect(center=rect.center)
            surf.blit(listenSurf, listenRect)
        elif icon:
            surf.blit(icon, rect)
        else:
            textSurf = self.labelFont.render(fallbackText, True, (240, 240, 245))
            textRect = textSurf.get_rect(center=rect.center)
            surf.blit(textSurf, textRect)

    def onResize(self, newSize: ScreenSize) -> None:
        self.screenSize = newSize
        self.scale = min(newSize[0] / self.baseW, newSize[1] / self.baseH)

        self.buttonFont = pygame.font.Font(None, self._s(28))
        self.labelFont = pygame.font.Font(None, self._s(32))

        for btn in [self.resetBtn, self.backBtn]:
            btn.setFont(self.buttonFont)

        self.iconSize = self._s(50)
        self.menuBg.onResize(newSize)
        self.panelSurf = None
        self._updateButtonPositions()
        self._updateKeyIcons()
        self.titleFont = pygame.font.Font(None, self._s(120))
        self.sectionFont = pygame.font.Font(None, self._s(48))

    def handleEvent(self, event: Event, inputEvent: "InputEvent | None" = None) -> None:
        if self.bListeningJump or self.bListeningSlide or self.bListeningRestart:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.bListeningJump = False
                    self.bListeningSlide = False
                    self.bListeningRestart = False
                else:
                    if self.bListeningJump:
                        keyBindings.jump = event.key
                        self.bListeningJump = False
                    elif self.bListeningSlide:
                        keyBindings.slide = event.key
                        self.bListeningSlide = False
                    elif self.bListeningRestart:
                        keyBindings.restart = event.key
                        self.bListeningRestart = False
                self._updateKeyIcons()
                return

        if event.type == pygame.MOUSEMOTION:
            self.bJumpHovered = self.jumpIconRect.collidepoint(event.pos)
            self.bSlideHovered = self.slideIconRect.collidepoint(event.pos)
            self.bRestartHovered = self.restartIconRect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.jumpIconRect.collidepoint(event.pos):
                self.bListeningJump = True
                return
            if self.slideIconRect.collidepoint(event.pos):
                self.bListeningSlide = True
                return
            if self.restartIconRect.collidepoint(event.pos):
                self.bListeningRestart = True
                return

        if self.resetBtn.handleEvent(event):
            keyBindings.reset()
            self._updateKeyIcons()
        elif self.backBtn.handleEvent(event):
            self.setState(GameState.MENU)

    def update(self, dt: float) -> None:
        self.menuBg.update(dt)
        self.time += dt
        self.titlePulse += dt * 3

    def draw(self, screen: Surface) -> None:
        self.menuBg.draw(screen)
        self._drawTitle(screen)
        self._drawControlsPanel(screen)
        self.resetBtn.draw(screen)
        self.backBtn.draw(screen)
