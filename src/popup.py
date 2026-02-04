import pygame
import random


class HitPopup:
    """Popup compact pour les notifications de succès/échec."""
    
    def __init__(self):
        self.active = False
        self.type = None
        self.timer = 0
        self.duration = 20  # frames (~0.33 seconde à 60 FPS)
        self.shake_intensity = 2
        
        try:
            self.font_big = pygame.font.SysFont("impact", 36)
            self.font_small = pygame.font.SysFont("arial", 16)
        except:
            self.font_big = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 16)
    
    def show(self, popup_type):
        """Active le popup avec le type 'success' ou 'fail'."""
        self.active = True
        self.type = popup_type
        self.timer = 0
    
    def update(self):
        """Met à jour le timer du popup."""
        if not self.active:
            return
        
        self.timer += 1
        if self.timer >= self.duration:
            self.active = False
    
    def draw(self, surface):
        """Dessine le popup compact avec effet shake."""
        if not self.active:
            return
        
        width, height = surface.get_size()
        
        # Effet shake léger
        progress = self.timer / self.duration
        shake_intensity = int(self.shake_intensity * (1 - progress))
        shake_x = random.randint(-shake_intensity, shake_intensity)
        shake_y = random.randint(-shake_intensity, shake_intensity)
        
        # Position centrale
        popup_x = width // 2 + shake_x
        popup_y = 150 + shake_y
        
        # Dimensions du popup compact
        popup_width = 200
        popup_height = 80
        
        # Transparence
        alpha = int(220 * (1 - progress * 0.7))
        
        if self.type == "success":
            bg_color = (20, 200, 80, alpha)
            title_text = "PERFECT!"
            subtitle_text = "+5 DMG"
            text_color = (255, 255, 255)
        else:
            bg_color = (200, 50, 50, alpha)
            title_text = "MISS!"
            subtitle_text = "COMBO x0"
            text_color = (255, 255, 255)
        
        # Créer le rectangle du popup
        popup_rect = pygame.Rect(
            popup_x - popup_width // 2,
            popup_y - popup_height // 2,
            popup_width,
            popup_height
        )
        
        # Fond du popup
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        pygame.draw.rect(popup_surface, bg_color, (0, 0, popup_width, popup_height), border_radius=10)
        pygame.draw.rect(popup_surface, (255, 255, 255, alpha), (0, 0, popup_width, popup_height), 3, border_radius=10)
        
        surface.blit(popup_surface, popup_rect.topleft)
        
        # Textes
        title = self.font_big.render(title_text, True, text_color)
        subtitle = self.font_small.render(subtitle_text, True, text_color)
        
        title_rect = title.get_rect(center=(popup_x, popup_y - 12))
        subtitle_rect = subtitle.get_rect(center=(popup_x, popup_y + 18))
        
        surface.blit(title, title_rect)
        surface.blit(subtitle, subtitle_rect)

