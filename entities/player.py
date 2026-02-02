import re
from enum import Enum, auto
from pathlib import Path

import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from settings import Color, ScreenSize

FRAMES_PATH: Path = Path(__file__).parent.parent / "assets" / "player" / "frames"


class PlayerState(Enum):
    RUNNING = auto()
    JUMPING = auto()
    SLIDING = auto()


class AnimationFrame:
    def __init__(self, surface: Surface, delay: float) -> None:
        self.surface: Surface = surface
        self.delay: float = delay


class Player(Sprite):
    GRAVITY: float = 1500.0
    JUMP_FORCE: float = -600.0
    SLIDE_DURATION: float = 0.5
    PLAYER_SCALE: float = 0.15

    def __init__(self, x: int, ground_y: int) -> None:
        super().__init__()

        self.frames: list[AnimationFrame] = self._load_frames()
        self.current_frame_index: int = 0
        self.animation_timer: float = 0.0

        if self.frames:
            self.width: int = self.frames[0].surface.get_width()
            self.height: int = self.frames[0].surface.get_height()
        else:
            self.width = 40
            self.height = 60

        self.slide_height: int = self.width

        self.image: Surface = self._get_current_frame()
        self.rect: Rect = self.image.get_rect()

        self.screen_size: ScreenSize = (800, 600)
        self.base_x: int = x
        self.ground_y: int = ground_y

        self.rect.midbottom = (x, ground_y)

        self.velocity_y: float = 0.0
        self.state: PlayerState = PlayerState.RUNNING
        self.slide_timer: float = 0.0

        self.on_ground: bool = True

    def _load_frames(self) -> list[AnimationFrame]:
        frames: list[AnimationFrame] = []
        pattern: re.Pattern[str] = re.compile(r"frame_(\d+)_delay-([\d.]+)s\.gif")

        if not FRAMES_PATH.exists():
            return [AnimationFrame(self._create_fallback_running_image(), 0.05)]

        frame_files: list[Path] = sorted(FRAMES_PATH.glob("*.gif"))

        for frame_file in frame_files:
            match: re.Match[str] | None = pattern.match(frame_file.name)
            if match:
                delay: float = float(match.group(2))
                try:
                    surface: Surface = pygame.image.load(str(frame_file)).convert_alpha()
                    scaled_width: int = int(surface.get_width() * self.PLAYER_SCALE)
                    scaled_height: int = int(surface.get_height() * self.PLAYER_SCALE)
                    scaled_surface: Surface = pygame.transform.scale(
                        surface, (scaled_width, scaled_height)
                    )
                    frames.append(AnimationFrame(scaled_surface, delay))
                except pygame.error:
                    continue

        if not frames:
            return [AnimationFrame(self._create_fallback_running_image(), 0.05)]

        return frames

    def _create_fallback_running_image(self) -> Surface:
        width: int = 40
        height: int = 60
        surface: Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        skin_color: Color = (210, 180, 140)
        shorts_color: Color = (200, 30, 30)
        shirt_color: Color = (255, 255, 255)

        pygame.draw.circle(surface, skin_color, (width // 2, 12), 10)
        pygame.draw.rect(surface, shirt_color, (width // 2 - 10, 22, 20, 18))
        pygame.draw.rect(surface, shorts_color, (width // 2 - 10, 38, 20, 12))
        pygame.draw.rect(surface, skin_color, (width // 2 - 8, 50, 6, 10))
        pygame.draw.rect(surface, skin_color, (width // 2 + 2, 50, 6, 10))
        pygame.draw.rect(surface, skin_color, (width // 2 - 18, 24, 8, 5))
        pygame.draw.rect(surface, skin_color, (width // 2 + 10, 24, 8, 5))

        return surface

    def _get_current_frame(self) -> Surface:
        if self.frames:
            return self.frames[self.current_frame_index].surface
        return self._create_fallback_running_image()

    def _get_slide_image(self) -> Surface:
        current: Surface = self._get_current_frame()
        rotated: Surface = pygame.transform.rotate(current, 90)
        return rotated

    def set_lanes(self, lanes: list[int]) -> None:
        pass

    def set_screen_size(self, size: ScreenSize) -> None:
        self.screen_size = size

    def set_ground_y(self, ground_y: int) -> None:
        self.ground_y = ground_y
        if self.on_ground:
            self.rect.bottom = ground_y

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_z, pygame.K_w):
                self._jump()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._slide()

    def _jump(self) -> None:
        if self.on_ground and self.state != PlayerState.SLIDING:
            self.velocity_y = self.JUMP_FORCE
            self.state = PlayerState.JUMPING
            self.on_ground = False
            self.image = self._get_current_frame()
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def _slide(self) -> None:
        if self.on_ground and self.state == PlayerState.RUNNING:
            self.state = PlayerState.SLIDING
            self.slide_timer = self.SLIDE_DURATION
            old_bottom: int = self.rect.bottom
            old_centerx: int = self.rect.centerx
            self.image = self._get_slide_image()
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.centerx = old_centerx

    def _end_slide(self) -> None:
        if self.state == PlayerState.SLIDING:
            self.state = PlayerState.RUNNING
            old_bottom: int = self.rect.bottom
            old_centerx: int = self.rect.centerx
            self.image = self._get_current_frame()
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.centerx = old_centerx

    def get_hitbox(self) -> Rect:
        if self.state == PlayerState.SLIDING:
            return self.rect.inflate(-10, -5)
        return self.rect.inflate(-10, -10)

    def _update_animation(self, dt: float) -> None:
        if not self.frames:
            return

        self.animation_timer += dt
        current_delay: float = self.frames[self.current_frame_index].delay

        if self.animation_timer >= current_delay:
            self.animation_timer = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

            if self.state == PlayerState.SLIDING:
                self.image = self._get_slide_image()
            else:
                self.image = self._get_current_frame()

    def update(self, dt: float) -> None:
        self._update_animation(dt)

        if self.state == PlayerState.JUMPING:
            self.velocity_y += self.GRAVITY * dt
            self.rect.y += int(self.velocity_y * dt)

            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                self.velocity_y = 0.0
                self.on_ground = True
                self.state = PlayerState.RUNNING

        elif self.state == PlayerState.SLIDING:
            self.slide_timer -= dt
            if self.slide_timer <= 0:
                self._end_slide()

        self.rect.centerx = self.base_x
