import pygame
from .config import WHITE


def load_image(path):
    """Charge une image avec transparence."""
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"❌ Erreur: {path} non trouvé")
        return None


def draw_text(surface, text, size, x, y, color=WHITE, bold=True):
    """Dessine du texte centré."""
    font = pygame.font.SysFont("arial", size, bold=bold)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)


def draw_bar(surface, x, y, width, height, fraction, color_fill, color_empty, color_border=WHITE):
    """Dessine une barre de progression."""
    fraction = max(0, min(fraction, 1.0))
    pygame.draw.rect(surface, color_empty, (x, y, width, height))
    pygame.draw.rect(surface, color_fill, (x, y, int(width * fraction), height))
    pygame.draw.rect(surface, color_border, (x, y, width, height), 2)
