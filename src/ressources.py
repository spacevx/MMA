"""
════════════════════════════════════════════════════════════════
  MODULE RESSOURCES - Gestion des images et sprites
════════════════════════════════════════════════════════════════
Charge et met en cache les images du jeu pour un rendu optimisé.
"""
import pygame
from .configuration import LARGEUR_ECRAN, HAUTEUR_ECRAN, CHEMIN_FOND, CHEMIN_ANNEAU, CHEMIN_JOUEUR, CHEMIN_BOSS, TAILLE_JOUEUR, TAILLE_BOSS, TAILLE_ANNEAU, NOIR
from .utilitaires import charger_image


class Ressources:
    """Charge et gère tous les sprites et images du jeu."""

    def __init__(self):
        """Initialiser les images avec mise à l'échelle appropriée."""
        # Fond plein écran
        fond = charger_image(CHEMIN_FOND)
        if fond:
            self.fond = pygame.transform.scale(fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        else:
            self.fond = None
        
        # Sprites avec transparence
        self.anneau = charger_image(CHEMIN_ANNEAU)
        if self.anneau:
            self.anneau = pygame.transform.scale(self.anneau, TAILLE_ANNEAU)
        
        self.joueur = charger_image(CHEMIN_JOUEUR)
        if self.joueur:
            self.joueur = pygame.transform.scale(self.joueur, TAILLE_JOUEUR)
        
        self.boss = charger_image(CHEMIN_BOSS)
        if self.boss:
            self.boss = pygame.transform.scale(self.boss, TAILLE_BOSS)

    def dessiner_fond(self, surface):
        """
        Dessiner le fond d'écran.
        Remplir avec du noir si pas d'image disponible.
        """
        surface.fill(NOIR)
        if self.fond:
            surface.blit(self.fond, (0, 0))

    def dessiner_anneau(self, surface, centre):
        """Afficher le ring (désactivé - le fond est déjà l'anneau)."""
        pass

    def dessiner_joueur(self, surface, position):
        """
        Afficher le sprite du joueur à la position donnée.
        Le sprite est centré sur cette position.
        """
        if self.joueur:
            rect = self.joueur.get_rect(center=position)
            surface.blit(self.joueur, rect)

    def dessiner_boss(self, surface, position):
        """
        Afficher le sprite du boss à la position donnée.
        Le sprite est centré sur cette position.
        """
        if self.boss:
            rect = self.boss.get_rect(center=position)
            surface.blit(self.boss, rect)
