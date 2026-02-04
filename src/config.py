import math
import pygame

# === ÉCRAN ===
SCREEN_W = 960
SCREEN_H = 540
FPS = 60

# === ASSETS ===
BG_PATH = "ring.png"
RING_PATH = "ring.png"
PLAYER_PATH = "player.png"
BOSS_PATH = "Combattant.png"

# === JOUEUR ===
PLAYER_HP = 10

# === PHASE 1: QTE ===
QTE_COUNT = 6
QTE_RADIUS = 50
QTE_TIME_LIMIT = 2.0
QTE_KEYS = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_z, pygame.K_x, pygame.K_c]
QTE_HIT_DAMAGE = 20
QTE_MISS_DAMAGE = 1

# === PHASE 2: ARROW RUSH ===
ARROW_CHALLENGE_COUNT = 25  # Plus de flèches pour une meilleure durée
ARROW_FALL_SPEED = 250  # pixels par seconde
ARROW_SPAWN_INTERVAL = 0.6  # secondes entre chaque flèche
ARROW_TARGET_Y = 420  # position Y de la zone cible
ARROW_HIT_WINDOW = 50  # pixels de tolérance pour réussir (zone encore plus réduite)
ARROW_SIZE = 50
ARROW_HIT_DAMAGE = 5  # Réduit car plus de flèches
ARROW_MISS_DAMAGE = 0  # Pas de perte de PV pour éviter faux positifs
ARROW_MISS_GRACE = 40  # marge de grâce avant de compter un miss
ARROW_GAME_DURATION = 60.0  # (non utilisé) ancien timer de phase
ARROW_DIFFICULTY_THRESHOLD_2 = 0.5  # À 50% des flèches réussies, on ajoute 2-touches
ARROW_DIFFICULTY_THRESHOLD_3 = 0.8  # À 80% des flèches réussies, on ajoute rarement 3-touches
ARROW_KEYS = {
    'Z': ('↑', (480, 50), (100, 150, 255)),   # Haut, bleu (AZERTY)
    'Q': ('←', (380, 50), (255, 150, 100)),   # Gauche, orange (AZERTY)
    'S': ('↓', (580, 50), (150, 255, 100)),   # Bas, vert
    'D': ('→', (680, 50), (255, 255, 100))    # Droite, jaune
}

BOSS_HP = 100

# === SPRITES ===
PLAYER_SIZE = (120, 120)
BOSS_SIZE = (120, 120)
RING_SIZE = (320, 320)

# === COULEURS ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 100)
BLUE = (80, 150, 230)
YELLOW = (255, 230, 60)
ORANGE = (240, 140, 60)
GRAY = (40, 40, 40)
