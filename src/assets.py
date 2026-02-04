import pygame
from .config import SCREEN_W, SCREEN_H, BG_PATH, RING_PATH, PLAYER_PATH, BOSS_PATH, PLAYER_SIZE, BOSS_SIZE, RING_SIZE, BLACK, GRAY
from .utils import load_image


class Assets:
    """Gère les images du jeu."""

    def __init__(self):
        # Background plein écran
        bg = load_image(BG_PATH)
        if bg:
            self.bg = pygame.transform.scale(bg, (SCREEN_W, SCREEN_H))
        else:
            self.bg = None
        
        # Sprites avec transparence
        self.ring = load_image(RING_PATH)
        if self.ring:
            self.ring = pygame.transform.scale(self.ring, RING_SIZE)
        
        self.player = load_image(PLAYER_PATH)
        if self.player:
            self.player = pygame.transform.scale(self.player, PLAYER_SIZE)
        
        self.boss = load_image(BOSS_PATH)
        if self.boss:
            self.boss = pygame.transform.scale(self.boss, BOSS_SIZE)

    def draw_bg(self, surface):
        """Remplit l'écran avec le background."""
        surface.fill(BLACK)
        if self.bg:
            surface.blit(self.bg, (0, 0))

    def draw_ring(self, surface, center):
        """Affiche le ring (désactivé - pas nécessaire)."""
        pass  # Le ring est déjà le background

    def draw_player(self, surface, pos):
        """Affiche le joueur."""
        if self.player:
            rect = self.player.get_rect(center=pos)
            surface.blit(self.player, rect)

    def draw_boss(self, surface, pos):
        """Affiche le boss."""
        if self.boss:
            rect = self.boss.get_rect(center=pos)
            surface.blit(self.boss, rect)
