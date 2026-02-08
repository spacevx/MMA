from enum import Enum, auto
from typing import Final

import pygame

from strings import windowTitle

# Don't try to change the resolution, code not responsive
width: Final[int] = 1280
height: Final[int] = 720
minWidth: Final[int] = 640
minHeight: Final[int] = 480

# TODO: Add a option in UI so we change the fps limit
fps: Final[int] = 60

title: Final[str] = windowTitle

displayFlags: Final[int] = pygame.RESIZABLE

Color = tuple[int, int, int]
ScreenSize = tuple[int, int]

black: Final[Color] = (0, 0, 0)
white: Final[Color] = (255, 255, 255)
red: Final[Color] = (200, 30, 30)
redBright: Final[Color] = (255, 50, 50)
gold: Final[Color] = (255, 215, 0)
darkGray: Final[Color] = (25, 25, 30)
darkGrayLight: Final[Color] = (40, 40, 50)


# State for knowing in which interface we are
class GameState(Enum):
    MENU = auto()
    LEVEL_SELECT = auto()
    GAME = auto()
    OPTIONS = auto()
    QUIT = auto()


obstacleSpawnEvent: Final[int] = pygame.USEREVENT + 1

bSoundEnabled: bool = True

levelCompleted: dict[int, bool] = {}
levelUnlocked: dict[int, bool] = {1: True}


def bIsLevelCompleted(levelId: int) -> bool:
    return levelCompleted.get(levelId, False)


def bIsLevelUnlocked(levelId: int) -> bool:
    if levelId == 1:
        return True
    return levelUnlocked.get(levelId, False)


def completeLevel(levelId: int) -> None:
    levelCompleted[levelId] = True
    levelUnlocked[levelId + 1] = True


def lastCompletedLevel() -> int | None:
    done = [k for k, v in levelCompleted.items() if v]
    return max(done) if done else None


def lastUnlockedLevel() -> int:
    unlocked = [k for k, v in levelUnlocked.items() if v]
    return max(unlocked) if unlocked else 1

# Controller data
JOY_DEADZONE: Final[float] = 0.3
JOY_AXIS_THRESHOLD: Final[float] = 0.5
DEFAULT_JOY_JUMP: Final[int] = 0
DEFAULT_JOY_SLIDE: Final[int] = 1
