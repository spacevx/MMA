"""
════════════════════════════════════════════════════════════════
  MODULE CONFIGURATION - Constantes du jeu
════════════════════════════════════════════════════════════════
Tous les paramètres globaux du jeu sont centralisés ici pour
faciliter les ajustements et l'équilibrage du gameplay.
"""
import pygame

# ════════════════════════════════════════════════════════════════
# ÉCRAN ET AFFICHAGE
# ════════════════════════════════════════════════════════════════
LARGEUR_ECRAN = 960
HAUTEUR_ECRAN = 540
IMAGES_PAR_SECONDE = 60

# ════════════════════════════════════════════════════════════════
# CHEMINS DES RESSOURCES
# ════════════════════════════════════════════════════════════════
CHEMIN_FOND = "ring.png"
CHEMIN_ANNEAU = "ring.png"
CHEMIN_JOUEUR = "player.png"
CHEMIN_BOSS = "Combattant.png"

# ════════════════════════════════════════════════════════════════
# POINTS DE VIE ET DÉGÂTS
# ════════════════════════════════════════════════════════════════
POINTS_VIE_JOUEUR = 10

# ════════════════════════════════════════════════════════════════
# PHASE 1: QTE (Quick Time Events)
# ════════════════════════════════════════════════════════════════
"""
La Phase 1 est un défi de Quick Time Events. Le joueur doit
cliquer au bon moment dans une zone circulaire avec la bonne touche.
"""
NOMBRE_DEFIS_QTE = 6
RAYON_QTE = 50  # Rayon de la zone de clic (pixels)
LIMITE_TEMPS_QTE = 2.0  # Temps imparti par défi (secondes)
TOUCHES_QTE = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_z, pygame.K_x, pygame.K_c]
DEGATS_HIT_QTE = 20  # Dégâts au boss par hit
DEGATS_MANQUE_QTE = 1  # Dégâts au joueur si manqué

# ════════════════════════════════════════════════════════════════
# PHASE 2: ARROW RUSH (Jeu de rythme)
# ════════════════════════════════════════════════════════════════
"""
La Phase 2 est un jeu de rythme où des flèches tombent et le
joueur doit appuyer au bon moment sur les touches correspondantes.
"""
NOMBRE_FLECHES_TOTAL = 25  # Nombre de flèches à frapper pour terminer
VITESSE_CHUTE_FLECHES = 250  # Pixels par seconde
INTERVALLE_SPAWN = 0.6  # Secondes entre chaque flèche
POSITION_Y_CIBLE = 420  # Position Y de la zone d'impact
FENETRE_HIT = 50  # Pixels de tolérance pour réussir (zone réduite)
TAILLE_FLECHE = 50  # Dimensions des carrés flèches
DEGATS_HIT_FLECHES = 5  # Dégâts au boss par hit
DEGATS_MANQUE_FLECHES = 0  # Dégâts au joueur si manqué
GRACE_MANQUE = 40  # Pixels de grâce avant de compter un miss
DUREE_JEU_FLECHES = 60.0  # (non utilisé) ancien timer
SEUIL_DIFFICULTE_2 = 0.5  # À 50% des flèches réussies
SEUIL_DIFFICULTE_3 = 0.8  # À 80% des flèches réussies

# Configuration des flèches AZERTY
TOUCHES_FLECHES = {
    'Z': ('↑', (480, 50), (100, 150, 255)),   # Haut, bleu (AZERTY)
    'Q': ('←', (380, 50), (255, 150, 100)),   # Gauche, orange (AZERTY)
    'S': ('↓', (580, 50), (150, 255, 100)),   # Bas, vert
    'D': ('→', (680, 50), (255, 255, 100))    # Droite, jaune
}

POINTS_VIE_BOSS = 100

# ════════════════════════════════════════════════════════════════
# SPRITES
# ════════════════════════════════════════════════════════════════
TAILLE_JOUEUR = (120, 120)
TAILLE_BOSS = (120, 120)
TAILLE_ANNEAU = (320, 320)

# ════════════════════════════════════════════════════════════════
# COULEURS
# ════════════════════════════════════════════════════════════════
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (220, 50, 50)
VERT = (50, 200, 100)
BLEU = (80, 150, 230)
JAUNE = (255, 230, 60)
ORANGE = (240, 140, 60)
GRIS = (40, 40, 40)
