from enum import Enum, auto

import pygame
from pygame import Rect, Surface
from pygame.math import Vector2

from entities.animation import AnimatedSprite, AnimationFrame, loadFrames
from paths import assetsPath

runningFramesPath = assetsPath / "player" / "running" / "frames"
slidingFramesPath = assetsPath / "player" / "sliding" / "frames"

class PlayerState(Enum):
    RUNNING = auto()
    JUMPING = auto()
    SLIDING = auto()

class Player(AnimatedSprite):
    gravity: float = 1500.0
    jumpForce: float = -600.0
    slideDuration: float = 0.5
    playerScale: float = 0.15
    slideScaleMult: float = 2.0

    def __init__(self, x: int, groundY: int) -> None:
        runningFrames = loadFrames(runningFramesPath, scale=self.playerScale)[116:132]
        self.runningHeight: int = runningFrames[0].surface.get_height()
        slidingTargetHeight = int(self.runningHeight * self.slideScaleMult)
        slidingFrames = loadFrames(slidingFramesPath, targetHeight=slidingTargetHeight)
        self.slidingHeight: int = slidingFrames[0].surface.get_height()
        self.slideYOffset: int = (self.slidingHeight - self.runningHeight) // 2
        super().__init__(x, groundY, runningFrames)

        self.runningFrames: list[AnimationFrame] = runningFrames
        self.slidingFrames: list[AnimationFrame] = slidingFrames
        self.groundY: int = groundY
        self.velocity: Vector2 = Vector2(0, 0)
        self.state: PlayerState = PlayerState.RUNNING
        self.slideTimer: float = 0.0
        self.bOnGround: bool = True

    def _setFrames(self, frames: list[AnimationFrame]) -> None:
        self.frames = frames
        self.frameIdx = 0
        self.animTimer = 0.0

    def setGroundY(self, groundY: int) -> None:
        self.groundY = groundY
        if self.bOnGround:
            self.rect.bottom = groundY

    def handleInput(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_z, pygame.K_w):
                self._jump()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._slide()

    def _jump(self) -> None:
        if self.bOnGround and self.state != PlayerState.SLIDING:
            self.velocity.y = self.jumpForce
            self.state = PlayerState.JUMPING
            self.bOnGround = False
            self.image = self._getFrame()
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def _slide(self) -> None:
        if self.bOnGround and self.state == PlayerState.RUNNING:
            self.state = PlayerState.SLIDING
            self.slideTimer = self.slideDuration
            oldCenterx = self.rect.centerx
            self._setFrames(self.slidingFrames)
            self.image = self._getFrame()
            self.rect = self.image.get_rect(centerx=oldCenterx, bottom=self.groundY + self.slideYOffset)

    def _endSlide(self) -> None:
        if self.state == PlayerState.SLIDING:
            self.state = PlayerState.RUNNING
            oldCenterx = self.rect.centerx
            self._setFrames(self.runningFrames)
            self.image = self._getFrame()
            self.rect = self.image.get_rect(centerx=oldCenterx, bottom=self.groundY)

    def getHitbox(self) -> Rect:
        if self.state == PlayerState.SLIDING:
            return self.rect.inflate(-10, -5)
        return self.rect.inflate(-10, -10)

    def _updateImage(self) -> None:
        self.image = self._getFrame()

    def update(self, dt: float) -> None:
        if self.updateAnimation(dt):
            self._updateImage()

        if self.state == PlayerState.JUMPING:
            self.velocity.y += self.gravity * dt
            self.rect.y += int(self.velocity.y * dt)

            if self.rect.bottom >= self.groundY:
                self.rect.bottom = self.groundY
                self.velocity.y = 0.0
                self.bOnGround = True
                self.state = PlayerState.RUNNING

        elif self.state == PlayerState.SLIDING:
            self.slideTimer -= dt
            if self.slideTimer <= 0:
                self._endSlide()
