from pathlib import Path

import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

ASSETS_PATH: Path = Path(__file__).parent.parent / "assets"


class Obstacle(Sprite):
    _image_cache: Surface | None = None

    def __init__(self, x: int, ground_y: int) -> None:
        super().__init__()
        self.speed: float = 350.0

        self.image: Surface = self._load_image()
        self.rect: Rect = self.image.get_rect(midbottom=(x, ground_y + 25))

    @classmethod
    def _load_image(cls) -> Surface:
        if cls._image_cache is None:
            image_path: Path = ASSETS_PATH / "lane.png"
            original: Surface = pygame.image.load(str(image_path)).convert_alpha()
            cls._image_cache = pygame.transform.scale(original, (350, 300))
        return cls._image_cache

    def update(self, dt: float) -> None:
        self.rect.x -= int(self.speed * dt)

    def is_off_screen(self) -> bool:
        return self.rect.right < 0
