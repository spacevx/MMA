"""
════════════════════════════════════════════════════════════════
  MODULE UTILITAIRES - Fonctions helpers
════════════════════════════════════════════════════════════════
Fonctions utilitaires pour le rendu texte, barres et chargement d'images.
"""
import pygame
from .configuration import BLANC


def charger_image(chemin):
    """
    Charger une image depuis un fichier avec support de la transparence.
    Retourne None si le fichier n'existe pas.
    """
    try:
        return pygame.image.load(chemin).convert_alpha()
    except Exception as e:
        print(f"❌ Erreur: {chemin} non trouvé")
        return None


def dessiner_texte(surface, texte, taille, x, y, couleur=BLANC, gras=True):
    """
    Dessiner du texte centré à la position (x, y).
    - texte: Chaîne à afficher
    - taille: Taille de la police en pixels
    - x, y: Position du centre du texte
    - couleur: Couleur RGB
    - gras: Utiliser la police en gras
    """
    police = pygame.font.SysFont("arial", taille, bold=gras)
    rendu = police.render(texte, True, couleur)
    rect = rendu.get_rect(center=(x, y))
    surface.blit(rendu, rect)


def dessiner_barre(surface, x, y, largeur, hauteur, fraction, couleur_remplie, couleur_vide, couleur_bordure=BLANC):
    """
    Dessiner une barre de progression.
    - x, y: Position du coin supérieur gauche
    - largeur, hauteur: Dimensions de la barre
    - fraction: Progression (0.0 à 1.0)
    - couleur_remplie: Couleur de la partie remplie
    - couleur_vide: Couleur de la partie vide
    - couleur_bordure: Couleur de la bordure
    """
    fraction = max(0, min(fraction, 1.0))
    pygame.draw.rect(surface, couleur_vide, (x, y, largeur, hauteur))
    pygame.draw.rect(surface, couleur_remplie, (x, y, int(largeur * fraction), hauteur))
    pygame.draw.rect(surface, couleur_bordure, (x, y, largeur, hauteur), 2)
