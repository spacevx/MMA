import math
import random
import pygame
from .config import (
    QTE_RADIUS, QTE_TIME_LIMIT, QTE_KEYS, QTE_COUNT,
    ARROW_CHALLENGE_COUNT, ARROW_FALL_SPEED, ARROW_SPAWN_INTERVAL, 
    ARROW_TARGET_Y, ARROW_HIT_WINDOW, ARROW_SIZE, ARROW_KEYS,
    ARROW_DIFFICULTY_THRESHOLD_2, ARROW_DIFFICULTY_THRESHOLD_3, ARROW_GAME_DURATION,
    ARROW_MISS_GRACE,
    BLUE, YELLOW, RED, GREEN, BLACK, WHITE, ORANGE, GRAY
)
from .utils import draw_text
from .popup import HitPopup


class QTE:
    """Phase 1: Cliquer au bon moment sur la bonne zone."""

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.done = 0
        self.total = QTE_COUNT
        self.popup = HitPopup()  # Popup style MMA pour QTE aussi
        self.reset_target()

    def reset_target(self):
        margin = 150
        self.x = random.randint(margin, self.screen_w - margin)
        self.y = random.randint(150, self.screen_h - 150)
        self.key = random.choice(QTE_KEYS)
        self.timer = QTE_TIME_LIMIT

    def update(self, dt, mouse_pos, key_pressed):
        self.timer -= dt
        self.popup.update()
        
        # Timeout
        if self.timer <= 0:
            self.popup.show("fail")
            self.reset_target()
            return "miss"
        
        # Vérifier interaction
        if key_pressed == self.key:
            mx, my = mouse_pos
            dist = math.hypot(mx - self.x, my - self.y)
            if dist <= QTE_RADIUS:
                self.popup.show("success")
                self.done += 1
                if self.done >= self.total:
                    return "complete"
                self.reset_target()
                return "hit"
            else:
                self.popup.show("fail")
                self.reset_target()
                return "miss"
        
        return None

    def draw(self, surface):
        # Cercle bleu (zone de clic)
        pygame.draw.circle(surface, BLUE, (self.x, self.y), QTE_RADIUS, 3)
        # Cercle jaune intérieur (indicateur)
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), QTE_RADIUS // 2, 2)
        # Texte touche avec fond blanc pour visibilité
        key_text = pygame.key.name(self.key).upper()
        font = pygame.font.Font(None, 28)
        text_surface = font.render(key_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        # Fond blanc derrière le texte
        pygame.draw.rect(surface, WHITE, text_rect.inflate(12, 8), border_radius=4)
        pygame.draw.rect(surface, BLACK, text_rect.inflate(12, 8), 1, border_radius=4)
        surface.blit(text_surface, text_rect)
        
        # Dessiner le popup
        self.popup.draw(surface)


class ArrowRush:
    """Phase 2: Arrow Rush - jeu de rythme avec minuteur."""

    def __init__(self):
        self.done = 0
        self.total = ARROW_CHALLENGE_COUNT
        self.arrows = []
        self.spawn_timer = 0.0
        self.elapsed_time = 0.0
        self.game_duration = ARROW_GAME_DURATION
        self.feedback_flash = {}
        self.combo = 0
        self.floating_texts = []  # Notifications flottantes (+5 / -1)
        self.miss_cooldown = 0.0  # Évite de perdre trop de PV en rafale
        self.popup = HitPopup()  # Popup style MMA
        # Pas de spawn initial - évite lag au démarrage

    def get_difficulty_multiplier(self):
        """Retourne le multiplicateur de difficulté basé sur les succès."""
        if self.done == 0:
            return 1
        success_ratio = self.done / self.total
        if success_ratio >= ARROW_DIFFICULTY_THRESHOLD_3:
            return 3
        elif success_ratio >= ARROW_DIFFICULTY_THRESHOLD_2:
            return 2
        return 1

    def spawn_arrow(self):
        """Crée une nouvelle flèche."""
        if len(self.arrows) < 20:
            # Pour l'instant, seulement des flèches simples (1 touche)
            selected_key = random.choice(list(ARROW_KEYS.keys()))
            
            self.arrows.append({
                'keys': [selected_key],
                'y': -50,
                'hit': False
            })

    def update(self, dt, pressed_key_this_frame):
        """Met à jour les flèches et gère les interactions."""
        self.elapsed_time += dt
        
        # Mise à jour du popup
        self.popup.update()
        
        # Cooldown pour éviter les pertes de PV trop rapides
        if self.miss_cooldown > 0:
            self.miss_cooldown = max(0.0, self.miss_cooldown - dt)
        
        # Spawn de nouvelles flèches
        self.spawn_timer += dt
        if self.spawn_timer >= ARROW_SPAWN_INTERVAL:
            self.spawn_arrow()
            self.spawn_timer = 0.0
        
        # Mise à jour des flèches
        missed_this_frame = False
        for arrow in self.arrows[:]:
            if not arrow['hit']:
                arrow['y'] += ARROW_FALL_SPEED * dt
            
            # Supprimer les flèches qui sont sorties de l'écran
            if arrow['y'] > ARROW_TARGET_Y + ARROW_HIT_WINDOW + ARROW_MISS_GRACE:
                self.arrows.remove(arrow)
                if not arrow['hit']:
                    # Flèche manquée - ne pas enlever de PV, juste réinitialiser le combo
                    self.combo = 0
        
        # Mise à jour des textes flottants
        for text in self.floating_texts[:]:
            text['time'] += dt
            text['y'] -= 60 * dt  # Montent vers le haut
            if text['time'] >= text['max_time']:
                self.floating_texts.remove(text)
        
        # Diminuer les flashs de feedback
        for key in list(self.feedback_flash.keys()):
            self.feedback_flash[key] -= dt
            if self.feedback_flash[key] <= 0:
                del self.feedback_flash[key]
        
        # Détection des touches UNE SEULE PAR FRAME (via event, pas get_pressed)
        if pressed_key_this_frame is not None:
            # Convertir le key_code pygame en clé ARROW_KEYS
            key_map = {
                pygame.K_z: 'Z',
                pygame.K_q: 'Q',
                pygame.K_s: 'S',
                pygame.K_d: 'D'
            }
            
            if pressed_key_this_frame in key_map:
                key = key_map[pressed_key_this_frame]
                result = self.check_hit(key)
                if result:
                    return result
        
        return None

    def check_hit(self, pressed_key):
        """Vérifie si le joueur a appuyé au bon moment."""
        # Trouver les flèches non-touchées pour cette touche dans la fenêtre
        valid_arrows = []
        for arrow in self.arrows:
            if pressed_key in arrow['keys'] and not arrow['hit']:
                distance = abs(arrow['y'] - ARROW_TARGET_Y)
                if distance <= ARROW_HIT_WINDOW:
                    valid_arrows.append((distance, arrow))
        
        # Si on a trouvé une ou plusieurs flèches dans la fenêtre
        if valid_arrows:
            # Prendre la plus proche
            valid_arrows.sort(key=lambda x: x[0])
            _, best_arrow = valid_arrows[0]
            
            # Marquer toutes les touches de cette flèche comme frappées
            for key in best_arrow['keys']:
                self.feedback_flash[key] = 0.3
            
            # Afficher le popup de succès
            self.popup.show("success")
            
            # Créer une notification flottante "+5"
            arrow_char, (base_x, _), color = ARROW_KEYS[pressed_key]
            self.floating_texts.append({
                'text': '+5',
                'x': base_x,
                'y': ARROW_TARGET_Y - 50,
                'time': 0.0,
                'max_time': 0.6,
                'color': GREEN
            })
            
            best_arrow['hit'] = True
            self.done += 1
            self.combo += 1
            
            if self.done >= self.total:
                return "complete"
            return "hit"
        
        # Mauvais timing - le joueur a appuyé mais pas sur une flèche valide
        # Ne montrer le popup fail que si on est proche de la zone cible
        closest_distance = float('inf')
        for arrow in self.arrows:
            if pressed_key in arrow['keys'] and not arrow['hit']:
                distance = abs(arrow['y'] - ARROW_TARGET_Y)
                if distance < closest_distance:
                    closest_distance = distance
        
        # Ne déclencher le popup fail que si on était proche (dans une zone élargie)
        if closest_distance < ARROW_HIT_WINDOW * 1.5:
            self.feedback_flash[pressed_key] = 0.2
            self.popup.show("fail")
            self.combo = 0
        
        return None

    def draw(self, surface, center):
        """Affiche le jeu Arrow Rush."""
        # Zone cible (ligne horizontale)
        pygame.draw.line(surface, WHITE, (300, ARROW_TARGET_Y), (660, ARROW_TARGET_Y), 4)
        pygame.draw.line(surface, YELLOW, (300, ARROW_TARGET_Y - 2), (660, ARROW_TARGET_Y - 2), 2)
        
        # Rectangles de hit zone pour chaque colonne
        for key, (arrow_char, (x, _), color) in ARROW_KEYS.items():
            # Dessiner la zone d'acceptation (ghost zone) en orange pour chaque colonne
            ghost_top = ARROW_TARGET_Y - ARROW_HIT_WINDOW
            ghost_height = ARROW_HIT_WINDOW * 2
            pygame.draw.rect(surface, ORANGE, (x - 5, ghost_top, ARROW_SIZE + 10, ghost_height), 1, border_radius=4)
            
            # Pulse d'animation lors du feedback
            is_success = key in self.feedback_flash
            if is_success:
                alpha = int(200 * (self.feedback_flash[key] / 0.3))
                flash_color = GREEN if self.feedback_flash[key] > 0.15 else RED
                flash_surf = pygame.Surface((ARROW_SIZE + 20, 80), pygame.SRCALPHA)
                pygame.draw.rect(flash_surf, (*flash_color, alpha), (0, 0, ARROW_SIZE + 20, 80), border_radius=8)
                surface.blit(flash_surf, (x - 10, ARROW_TARGET_Y - 40))
            
            # Zone de réception avec bordure animée si feedback
            border_color = color
            border_width = 3
            if is_success:
                pulse = 1.0 + 0.3 * (self.feedback_flash[key] / 0.3)
                border_width = max(2, int(3 * pulse))
                border_color = GREEN if self.feedback_flash[key] > 0.15 else RED
            
            pygame.draw.rect(surface, border_color, (x, ARROW_TARGET_Y - 25, ARROW_SIZE, ARROW_SIZE), border_width, border_radius=5)
            draw_text(surface, key, 18, x + ARROW_SIZE // 2, ARROW_TARGET_Y + 60, color, bold=True)
        
        # Dessiner les flèches qui tombent
        for arrow in self.arrows:
            if arrow['hit']:
                continue  # Ne pas dessiner les flèches déjà touchées
            
            # Boucler sur chaque touche de la flèche
            for idx, key in enumerate(arrow['keys']):
                arrow_char, (base_x, _), color = ARROW_KEYS[key]
                
                # Décalage horizontal si plusieurs touches (pour les afficher côte à côte)
                x_offset = 0
                if len(arrow['keys']) == 2:
                    x_offset = -25 if idx == 0 else 25
                elif len(arrow['keys']) == 3:
                    x_offset = -25 if idx == 0 else (0 if idx == 1 else 25)
                
                x = base_x + x_offset
                y = arrow['y']
                
                # Effet de proximité (plus lumineux près de la cible)
                distance_to_target = abs(y - ARROW_TARGET_Y)
                if distance_to_target < 60:
                    brightness = 1.0 + (1.0 - distance_to_target / 60) * 0.5
                    color = tuple(min(255, int(c * brightness)) for c in color)
                
                # Dessiner la flèche
                pygame.draw.rect(surface, color, (x, y, ARROW_SIZE, ARROW_SIZE), border_radius=5)
                pygame.draw.rect(surface, WHITE, (x, y, ARROW_SIZE, ARROW_SIZE), 2, border_radius=5)
                draw_text(surface, arrow_char, 32, x + ARROW_SIZE // 2, y + ARROW_SIZE // 2, BLACK, bold=True)
        
        # Instructions et stats
        draw_text(surface, "Appuie sur Z/Q/S/D quand les flèches atteignent la zone!", 16, 480, 100, WHITE)
        draw_text(surface, f"Combo: {self.combo}", 18, 50, 50, YELLOW, bold=True)
        
        # Dessiner les textes flottants
        for text_obj in self.floating_texts:
            progress = text_obj['time'] / text_obj['max_time']
            alpha = int(255 * (1 - progress))  # Disparaît progressivement
            
            # Créer une surface avec le texte
            font = pygame.font.Font(None, 48)
            text_surface = font.render(text_obj['text'], True, text_obj['color'])
            
            # Ajouter une transparence
            text_surface.set_alpha(alpha)
            
            # Positionner et afficher
            text_rect = text_surface.get_rect(center=(text_obj['x'], int(text_obj['y'])))
            surface.blit(text_surface, text_rect)
        
        # Dessiner le popup par-dessus tout
        self.popup.draw(surface)
