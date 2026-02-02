from enum import Enum, auto
from pathlib import Path

import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from settings import Color

ASSETS_PATH: Path = Path(__file__).parent.parent / "assets"


class ObstacleType(Enum):
    LOW = auto()
    HIGH = auto()


class Obstacle(Sprite):
    _texture: Surface | None = None
    _low_image_cache: Surface | None = None
    _high_image_cache: Surface | None = None

    LOW_WIDTH: int = 120
    LOW_HEIGHT: int = 100
    HIGH_WIDTH: int = 140
    HIGH_HEIGHT: int = 110

    def __init__(self, x: int, ground_y: int, obstacle_type: ObstacleType) -> None:
        super().__init__()
        self.obstacle_type: ObstacleType = obstacle_type
        self.speed: float = 400.0
        self.ground_y: int = ground_y

        self.image: Surface = self._get_image(obstacle_type)
        self.rect: Rect = self._position_rect(x, ground_y, obstacle_type)

    @classmethod
    def clear_cache(cls) -> None:
        cls._texture = None
        cls._low_image_cache = None
        cls._high_image_cache = None

    @classmethod
    def _load_texture(cls) -> Surface | None:
        if cls._texture is None:
            try:
                image_path: Path = ASSETS_PATH / "lane.png"
                cls._texture = pygame.image.load(str(image_path)).convert_alpha()
            except (pygame.error, FileNotFoundError):
                cls._texture = None
        return cls._texture

    @classmethod
    def _get_image(cls, obstacle_type: ObstacleType) -> Surface:
        if obstacle_type == ObstacleType.LOW:
            return cls._get_low_image()
        return cls._get_high_image()

    @classmethod
    def _create_obstacle_surface(cls, width: int, height: int, flip: bool = False) -> Surface:
        surface: Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        texture: Surface | None = cls._load_texture()

        if texture is not None:
            tex_width: int = texture.get_width()
            tex_height: int = texture.get_height()

            scale_factor: float = min(width / tex_width, height / tex_height) * 0.95
            new_width: int = int(tex_width * scale_factor)
            new_height: int = int(tex_height * scale_factor)

            scaled_texture: Surface = pygame.transform.smoothscale(texture, (new_width, new_height))

            if flip:
                scaled_texture = pygame.transform.flip(scaled_texture, False, True)

            x_offset: int = (width - new_width) // 2
            y_offset: int = (height - new_height) // 2

            surface.blit(scaled_texture, (x_offset, y_offset))
        else:
            surface = cls._create_fallback(width, height, flip)

        return surface

    @classmethod
    def _get_low_image(cls) -> Surface:
        if cls._low_image_cache is None:
            cls._low_image_cache = cls._create_obstacle_surface(cls.LOW_WIDTH, cls.LOW_HEIGHT, flip=False)
        return cls._low_image_cache

    @classmethod
    def _get_high_image(cls) -> Surface:
        if cls._high_image_cache is None:
            cls._high_image_cache = cls._create_obstacle_surface(cls.HIGH_WIDTH, cls.HIGH_HEIGHT, flip=True)
        return cls._high_image_cache

    @classmethod
    def _create_fallback(cls, width: int, height: int, flip: bool) -> Surface:
        surface: Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        if not flip:
            wood_color: Color = (139, 90, 43)
            dark_wood: Color = (101, 67, 33)
            pygame.draw.rect(surface, wood_color, (10, 10, width - 20, height - 20))
            pygame.draw.rect(surface, dark_wood, (10, 10, width - 20, height - 20), 4)
            pygame.draw.rect(surface, dark_wood, (0, height - 20, 20, 20))
            pygame.draw.rect(surface, dark_wood, (width - 20, height - 20, 20, 20))
        else:
            metal_color: Color = (150, 150, 160)
            dark_metal: Color = (100, 100, 110)
            pygame.draw.rect(surface, metal_color, (10, 10, width - 20, height - 20))
            pygame.draw.rect(surface, dark_metal, (10, 10, width - 20, height - 20), 4)
            pygame.draw.rect(surface, dark_metal, (0, 0, 20, 20))
            pygame.draw.rect(surface, dark_metal, (width - 20, 0, 20, 20))

        return surface

    def _position_rect(self, x: int, ground_y: int, obstacle_type: ObstacleType) -> Rect:
        rect: Rect = self.image.get_rect()
        if obstacle_type == ObstacleType.LOW:
            rect.midbottom = (x, ground_y)
        else:
            rect.midbottom = (x, ground_y - 60)
        return rect

    def get_hitbox(self) -> Rect:
        return self.rect.inflate(-20, -15)

    def update(self, dt: float) -> None:
        self.rect.x -= int(self.speed * dt)

    def is_off_screen(self) -> bool:
        return self.rect.right < -50
