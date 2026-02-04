"""
════════════════════════════════════════════════════════════════
  MODULE NOTIFICATION - Popups de feedback (style MMA)
════════════════════════════════════════════════════════════════
Affiche des notifications compactes en haut de l'écran pour
récompenser le joueur (PERFECT! / MISS!) avec des effets visuels.
"""
import pygame
import random


class NotificationRésultat:
    """Popup compact pour les notifications de succès/échec (style MMA)."""
    
    def __init__(self):
        """Initialiser la notification."""
        self.active = False
        self.type = None
        self.minuteur = 0
        self.duree = 20  # frames (~0.33 secondes à 60 FPS)
        self.intensite_secousse = 2
        
        # Charger les polices
        try:
            self.police_grande = pygame.font.SysFont("impact", 36)
            self.police_petite = pygame.font.SysFont("arial", 16)
        except:
            self.police_grande = pygame.font.Font(None, 36)
            self.police_petite = pygame.font.Font(None, 16)
    
    def afficher(self, type_notification):
        """
        Activer la notification avec le type 'succes' ou 'echec'.
        - type_notification: "succes" pour vert ou "echec" pour rouge
        """
        self.active = True
        self.type = type_notification
        self.minuteur = 0
    
    def actualiser(self):
        """
        Mettre à jour le minuteur de la notification.
        La notification s'éteint après 'duree' frames.
        """
        if not self.active:
            return
        
        self.minuteur += 1
        if self.minuteur >= self.duree:
            self.active = False
    
    def dessiner(self, surface):
        """
        Dessiner la notification avec effets de shake et fade-out.
        Affichée en haut-centre de l'écran avec style MMA.
        """
        if not self.active:
            return
        
        largeur, hauteur = surface.get_size()
        
        # Effet de secousse léger (shake)
        progression = self.minuteur / self.duree
        intensite_secousse = int(self.intensite_secousse * (1 - progression))
        decalage_x = random.randint(-intensite_secousse, intensite_secousse)
        decalage_y = random.randint(-intensite_secousse, intensite_secousse)
        
        # Position centrale
        popup_x = largeur // 2 + decalage_x
        popup_y = 150 + decalage_y
        
        # Dimensions du popup compact
        largeur_popup = 200
        hauteur_popup = 80
        
        # Transparence (fade-out progressif)
        transparence = int(220 * (1 - progression * 0.7))
        
        # Configuration selon le type
        if self.type == "succes":
            couleur_fond = (20, 200, 80, transparence)
            texte_titre = "PERFECT!"
            texte_sous = "+5 DMG"
            couleur_texte = (255, 255, 255)
        else:  # echec
            couleur_fond = (200, 50, 50, transparence)
            texte_titre = "MISS!"
            texte_sous = "COMBO x0"
            couleur_texte = (255, 255, 255)
        
        # Créer le rectangle du popup
        rect_popup = pygame.Rect(
            popup_x - largeur_popup // 2,
            popup_y - hauteur_popup // 2,
            largeur_popup,
            hauteur_popup
        )
        
        # Fond semi-transparent avec bordure arrondie
        surface_popup = pygame.Surface((largeur_popup, hauteur_popup), pygame.SRCALPHA)
        pygame.draw.rect(surface_popup, couleur_fond, (0, 0, largeur_popup, hauteur_popup), border_radius=10)
        pygame.draw.rect(surface_popup, (255, 255, 255, transparence), (0, 0, largeur_popup, hauteur_popup), 3, border_radius=10)
        
        surface.blit(surface_popup, rect_popup.topleft)
        
        # Afficher le texte du popup
        titre = self.police_grande.render(texte_titre, True, couleur_texte)
        sous = self.police_petite.render(texte_sous, True, couleur_texte)
        
        rect_titre = titre.get_rect(center=(popup_x, popup_y - 12))
        rect_sous = sous.get_rect(center=(popup_x, popup_y + 18))
        
        surface.blit(titre, rect_titre)
        surface.blit(sous, rect_sous)
