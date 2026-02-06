from __future__ import annotations

from dataclasses import dataclass

import pygame
from pygame.sprite import Group

from entities import Player, PlayerState, Chaser, Obstacle, BaseObstacle, FallingCage, CageState


@dataclass
class CollisionResult:
    bHitObstacle: bool = False
    bHitCage: bool = False
    bCaught: bool = False
    trappingCage: FallingCage | None = None


class GameCollision:
    baseW: int = 1920
    baseH: int = 1080

    def __init__(self, screenSize: tuple[int, int]) -> None:
        self.scale = min(screenSize[0] / self.baseW, screenSize[1] / self.baseH)

    # Scaling func
    def _s(self, val: int) -> int:
        return max(1, int(val * self.scale))

    def onResize(self, screenSize: tuple[int, int]) -> None:
        self.scale = min(screenSize[0] / self.baseW, screenSize[1] / self.baseH)


    # When a player hit obstacle, returns true if its a real hit (not jumping over it)
    def _obstacleCallback(self, player: Player, obstacle: Obstacle) -> bool:
        playerHitbox = player.getHitbox()
        obstacleHitbox = obstacle.getHitbox()

        if not playerHitbox.colliderect(obstacleHitbox):
            return False

        if player.state == PlayerState.JUMPING:
            if playerHitbox.bottom < obstacleHitbox.top + self._s(15):
                return False

        return True

    # Same but for falling cages, will ignore if it's a falling cage (or has the immunit window)
    # Btw i need to rework the immunity window, rn this system is pure shit
    def _cageCallback(self, player: Player, cage: FallingCage) -> bool:
        if cage.state != CageState.FALLING:
            return False

        playerHitbox = player.getHitbox()
        cageHitbox = cage.getHitbox()

        if not playerHitbox.colliderect(cageHitbox):
            return False

        if player.isInImmunityWindow():
            return False

        return True

    # Run every frame and we are checking if the player hit a obstacle/cage or was caught by the chaser (it's like the update func)
    def check(self, player: Player, chaser: Chaser | None, obstacles: Group[Obstacle],
              cages: Group[FallingCage], bInvincible: bool) -> CollisionResult:
        result = CollisionResult()

        if bInvincible:
            if chaser and chaser.hasCaughtPlayer(player.getHitbox()):
                result.bCaught = True
            return result

        hitObstacles: list[Obstacle] = pygame.sprite.spritecollide(
            player, obstacles, dokill=False, collided=self._obstacleCallback
        )

        if hitObstacles:
            result.bHitObstacle = True
            hitObstacles[0].kill()

        hitCages: list[FallingCage] = pygame.sprite.spritecollide(
            player, cages, dokill=False, collided=self._cageCallback
        )

        if hitCages:
            result.bHitCage = True
            result.trappingCage = hitCages[0]

        if chaser and chaser.hasCaughtPlayer(player.getHitbox()):
            result.bCaught = True

        return result

    # Func only for level 3, allow us to know if the laser hit a obstacle
    def checkLaserHit(self, playerX: int, playerY: int, obstacles: Group[BaseObstacle],
                      laserRange: float) -> BaseObstacle | None:
        from entities.obstacle.geometric import GeometricObstacle

        laserRect = pygame.Rect(playerX, playerY - 15, int(laserRange), 30)

        for obstacle in obstacles:
            if isinstance(obstacle, GeometricObstacle):
                if laserRect.colliderect(obstacle.getHitbox()):
                    return obstacle
        return None
