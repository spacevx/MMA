import math
from typing import Callable

import pygame
import pygame_gui
from pygame import Surface
from pygame.event import Event
from pygame.font import Font
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID

from settings import WIDTH, HEIGHT, DARK_GRAY, GOLD, RED, WHITE, GameState, Color, ScreenSize
from strings import MENU_TITLE, MENU_SUBTITLE, BTN_START, BTN_OPTIONS, BTN_QUIT


class MainMenu:
    def __init__(self, set_state_callback: Callable[[GameState], None]) -> None:
        self.set_state: Callable[[GameState], None] = set_state_callback
        self.screen_size: ScreenSize = (WIDTH, HEIGHT)

        self.manager: UIManager = UIManager(self.screen_size, theme_path=None)
        self._setup_theme()

        self.background: Surface = self._create_background(WIDTH, HEIGHT)

        self.start_btn: UIButton | None = None
        self.options_btn: UIButton | None = None
        self.quit_btn: UIButton | None = None
        self._create_buttons()

        self.title_font: Font = pygame.font.Font(None, 120)
        self.subtitle_font: Font = pygame.font.Font(None, 36)

    def _setup_theme(self) -> None:
        self.manager.get_theme().load_theme({
            "button": {
                "colours": {
                    "normal_bg": "#C81E1E",
                    "hovered_bg": "#FF3232",
                    "active_bg": "#FF3232",
                    "normal_border": "#C81E1E",
                    "hovered_border": "#FFD700",
                    "active_border": "#FFD700",
                    "normal_text": "#FFFFFF",
                    "hovered_text": "#FFFFFF",
                    "active_text": "#FFFFFF"
                },
                "misc": {
                    "shape": "rounded_rectangle",
                    "shape_corner_radius": "8",
                    "border_width": "3"
                }
            }
        })

    def _get_button_rects(self) -> list[pygame.Rect]:
        width: int = self.screen_size[0]
        height: int = self.screen_size[1]
        button_width: int = 320
        button_height: int = 50
        center_x: int = (width - button_width) // 2
        return [
            pygame.Rect(center_x, int(height * 0.50), button_width, button_height),
            pygame.Rect(center_x, int(height * 0.62), button_width, button_height),
            pygame.Rect(center_x, int(height * 0.74), button_width, button_height),
        ]

    def _create_buttons(self) -> None:
        rects: list[pygame.Rect] = self._get_button_rects()

        self.start_btn = UIButton(
            relative_rect=rects[0],
            text=BTN_START,
            manager=self.manager,
            object_id=ObjectID(object_id="#start_btn")
        )

        self.options_btn = UIButton(
            relative_rect=rects[1],
            text=BTN_OPTIONS,
            manager=self.manager,
            object_id=ObjectID(object_id="#options_btn")
        )

        self.quit_btn = UIButton(
            relative_rect=rects[2],
            text=BTN_QUIT,
            manager=self.manager,
            object_id=ObjectID(object_id="#quit_btn")
        )

    def _update_button_positions(self) -> None:
        rects: list[pygame.Rect] = self._get_button_rects()
        if self.start_btn:
            self.start_btn.set_relative_position((rects[0].x, rects[0].y))
        if self.options_btn:
            self.options_btn.set_relative_position((rects[1].x, rects[1].y))
        if self.quit_btn:
            self.quit_btn.set_relative_position((rects[2].x, rects[2].y))

    def on_resize(self, new_size: ScreenSize) -> None:
        self.screen_size = new_size
        self.manager.set_window_resolution(new_size)
        self.background = self._create_background(new_size[0], new_size[1])
        self._update_button_positions()

    def _create_background(self, width: int, height: int) -> Surface:
        surface: Surface = pygame.Surface((width, height))

        for y in range(height):
            factor: float = 1 - abs(y - height // 2) / (height // 2) * 0.3
            color: Color = (
                int(DARK_GRAY[0] * factor),
                int(DARK_GRAY[1] * factor),
                int(DARK_GRAY[2] * factor)
            )
            pygame.draw.line(surface, color, (0, y), (width, y))

        self._draw_spotlight(surface, width, height)
        self._draw_octagon(surface, width, height)
        self._draw_cage_fence(surface, width, height)

        return surface

    def _draw_spotlight(self, surface: Surface, width: int, height: int) -> None:
        center_x: int = width // 2
        for y in range(height // 2):
            radius: int = int(y * 0.8)
            alpha: int = max(0, 30 - y // 10)
            if alpha > 0 and radius > 0:
                spotlight: Surface = pygame.Surface((radius * 2, 2), pygame.SRCALPHA)
                spotlight.fill((255, 255, 255, alpha))
                surface.blit(spotlight, (center_x - radius, y))

    def _draw_octagon(self, surface: Surface, width: int, height: int) -> None:
        center_x: int = width // 2
        center_y: int = height // 2 + 50
        radius: int = min(200, min(width, height) // 3)

        points: list[tuple[float, float]] = []
        for i in range(8):
            angle: float = math.pi / 8 + i * math.pi / 4
            x: float = center_x + radius * math.cos(angle)
            y: float = center_y + radius * math.sin(angle)
            points.append((x, y))

        octagon_color: Color = (60, 60, 70)
        pygame.draw.polygon(surface, octagon_color, points, 3)

        inner_points: list[tuple[float, float]] = []
        inner_radius: int = radius - 20
        for i in range(8):
            angle: float = math.pi / 8 + i * math.pi / 4
            x: float = center_x + inner_radius * math.cos(angle)
            y: float = center_y + inner_radius * math.sin(angle)
            inner_points.append((x, y))

        pygame.draw.polygon(surface, (50, 50, 60), inner_points, 2)

    def _draw_cage_fence(self, surface: Surface, width: int, height: int) -> None:
        fence_color: Color = (45, 45, 55)

        for y in range(0, height, 20):
            for x in range(0, 40, 20):
                pygame.draw.line(surface, fence_color, (x, y), (x + 10, y + 10), 1)
                pygame.draw.line(surface, fence_color, (x + 10, y + 10), (x, y + 20), 1)

        for y in range(0, height, 20):
            for x in range(width - 40, width, 20):
                pygame.draw.line(surface, fence_color, (x, y), (x + 10, y + 10), 1)
                pygame.draw.line(surface, fence_color, (x + 10, y + 10), (x, y + 20), 1)

    def handle_event(self, event: Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_btn:
                self.set_state(GameState.GAME)
            elif event.ui_element == self.options_btn:
                self.set_state(GameState.OPTIONS)
            elif event.ui_element == self.quit_btn:
                self.set_state(GameState.QUIT)

    def update(self, dt: float) -> None:
        self.manager.update(dt)

    def draw(self, screen: Surface) -> None:
        width: int = self.screen_size[0]
        height: int = self.screen_size[1]

        screen.blit(self.background, (0, 0))

        title_y: int = int(height * 0.20)
        subtitle_y: int = int(height * 0.30)

        shadow_surface: Surface = self.title_font.render(MENU_TITLE, True, RED)
        shadow_rect = shadow_surface.get_rect(center=(width // 2 + 4, title_y + 4))
        screen.blit(shadow_surface, shadow_rect)

        title_surface: Surface = self.title_font.render(MENU_TITLE, True, GOLD)
        title_rect = title_surface.get_rect(center=(width // 2, title_y))
        screen.blit(title_surface, title_rect)

        subtitle_surface: Surface = self.subtitle_font.render(MENU_SUBTITLE, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(width // 2, subtitle_y))
        screen.blit(subtitle_surface, subtitle_rect)

        self.manager.draw_ui(screen)
