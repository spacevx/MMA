import sys
import pygame
from .config import *
from .stages import QTE, ArrowRush
from .assets import Assets
from .utils import draw_text, draw_bar


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Easter Egg - Boss Fight")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        
        self.ring_center = (SCREEN_W // 2, SCREEN_H // 2)
        self.player_pos = (SCREEN_W - 100, SCREEN_H // 2 + 50)
        self.boss_pos = (100, SCREEN_H // 2 + 50)
        self.pressed_key_this_frame = None  # Stocke UNE SEULE touche par frame
        
        self.reset()

    def reset(self):
        """Réinitialise une partie."""
        self.stage = "menu"
        self._init_common_state()
        self._start_qte_phase()

    def _init_common_state(self):
        self.player_hp = PLAYER_HP
        self.boss_hp = BOSS_HP
        self.feedback = ""
        self.feedback_time = 0.0

    def _start_qte_phase(self):
        self.qte = QTE(SCREEN_W, SCREEN_H)

    def _start_arrow_phase(self):
        self.arrows = ArrowRush()

    def handle_events(self):
        """Gère les événements."""
        self.pressed_key_this_frame = None  # Réinitialise à chaque frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN and self.stage == "menu":
                    self.stage = "qte_phase1"
                if event.key == pygame.K_r and self.stage in ("win", "lose"):
                    self.reset()
                # Capturer UNE SEULE touche par frame pour éviter les multiples simultanées
                if self.pressed_key_this_frame is None and event.key in [pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.pressed_key_this_frame = event.key
        return True

    def update(self, dt):
        """Met à jour la logique du jeu."""
        self.feedback_time -= dt
        
        if self.stage == "qte_phase1":
            result = self.qte.update(dt, pygame.mouse.get_pos(), self.get_key_pressed())
            
            if result == "hit":
                self.boss_hp -= QTE_HIT_DAMAGE
                self.feedback = "✓ Touché!"
                self.feedback_time = 0.3
            elif result == "miss":
                self.player_hp -= QTE_MISS_DAMAGE
                self.feedback = "✗ Manqué!"
                self.feedback_time = 0.3
            elif result == "complete":
                # Régénère le boss ET le joueur pour la phase 2
                self.boss_hp = BOSS_HP
                self.player_hp = PLAYER_HP
                self.stage = "arrow_phase2"
                self._start_arrow_phase()
                self.feedback = ""
            
            if self.player_hp <= 0:
                self.stage = "lose"
                self.feedback = ""
        
        elif self.stage == "arrow_phase2":
            result = self.arrows.update(dt, self.pressed_key_this_frame)
            
            if result == "hit":
                self.boss_hp -= ARROW_HIT_DAMAGE
                self.feedback = "🎯 Hit!"
                self.feedback_time = 0.3
            elif result == "miss":
                self.player_hp -= ARROW_MISS_DAMAGE
                self.feedback = "✗ Miss!"
                self.feedback_time = 0.3
            elif result == "complete":
                self.stage = "win"
                self.feedback = ""
            
            if self.player_hp <= 0:
                self.stage = "lose"
                self.feedback = ""
            
            if self.boss_hp <= 0:
                self.stage = "win"
                self.feedback = ""
            elif result == "complete":
                self.stage = "win"
                self.feedback = ""
            
            if self.player_hp <= 0:
                self.stage = "lose"
                self.feedback = ""
            
            if self.boss_hp <= 0:
                self.stage = "win"
                self.feedback = ""

    def get_key_pressed(self):
        """Retourne la touche appuyée."""
        keys = pygame.key.get_pressed()
        for key in QTE_KEYS:
            if keys[key]:
                return key
        return None

    def draw(self):
        """Dessine l'écran."""
        self.assets.draw_bg(self.screen)
        self.assets.draw_ring(self.screen, self.ring_center)
        self.assets.draw_boss(self.screen, self.boss_pos)
        self.assets.draw_player(self.screen, self.player_pos)
        
        # Barres de vie
        draw_bar(self.screen, 20, SCREEN_H - 60, 180, 14, self.boss_hp / BOSS_HP, RED, GRAY)
        draw_text(self.screen, "Boss", 14, 20, SCREEN_H - 42, WHITE)
        
        draw_bar(self.screen, SCREEN_W - 200, SCREEN_H - 60, 180, 14, self.player_hp / PLAYER_HP, GREEN, GRAY)
        draw_text(self.screen, "Joueur", 14, SCREEN_W - 200, SCREEN_H - 42, WHITE)
        
        # Stages
        if self.stage == "menu":
            draw_text(self.screen, "BOSS FIGHT", 48, SCREEN_W // 2, 100, YELLOW)
            draw_text(self.screen, "Phase 1: QTE | Phase 2: Arrow Rush", 20, SCREEN_W // 2, 160, WHITE)
            draw_text(self.screen, "Appuie sur ENTRÉE", 18, SCREEN_W // 2, 220, ORANGE)
        
        elif self.stage == "qte_phase1":
            draw_text(self.screen, f"QTE Phase 1 ({self.qte.done}/{self.qte.total})", 20, 20, 20, WHITE)
            draw_text(self.screen, "Mets la souris dans le cercle et appuie sur la touche", 16, SCREEN_W // 2, 50, WHITE)
            self.qte.draw(self.screen)
            
            # Barre temps
            progress = self.qte.timer / QTE_TIME_LIMIT
            draw_bar(self.screen, SCREEN_W // 2 - 100, SCREEN_H - 30, 200, 10, progress, ORANGE, GRAY)
        
        elif self.stage == "arrow_phase2":
            draw_text(self.screen, f"Arrow Rush ({self.arrows.done}/{self.arrows.total})", 20, 20, 20, WHITE)
            self.arrows.draw(self.screen, self.ring_center)
            
            # Barre de vie du boss (pas de joueur en phase 2)
            draw_bar(self.screen, 20, SCREEN_H - 60, 180, 14, self.boss_hp / BOSS_HP, RED, GRAY)
            draw_text(self.screen, "Boss", 14, 20, SCREEN_H - 42, WHITE)
        
        elif self.stage == "win":
            draw_text(self.screen, "VICTOIRE!", 48, SCREEN_W // 2, SCREEN_H // 2 - 40, YELLOW)
            draw_text(self.screen, "Easter Egg terminé!", 24, SCREEN_W // 2, SCREEN_H // 2 + 20, GREEN)
            draw_text(self.screen, "Appuie sur R pour rejouer", 16, SCREEN_W // 2, SCREEN_H // 2 + 70, WHITE)
        
        elif self.stage == "lose":
            draw_text(self.screen, "DÉFAITE", 48, SCREEN_W // 2, SCREEN_H // 2 - 40, RED)
            draw_text(self.screen, "Tu as perdu tous tes PV!", 24, SCREEN_W // 2, SCREEN_H // 2 + 20, RED)
            draw_text(self.screen, "Appuie sur R pour réessayer", 16, SCREEN_W // 2, SCREEN_H // 2 + 70, WHITE)
        
        # Feedback
        if self.feedback_time > 0:
            draw_text(self.screen, self.feedback, 22, SCREEN_W // 2, 90, WHITE)
        
        pygame.display.flip()

    def run(self):
        """Boucle principale."""
        running = True
        while running:
            running = self.handle_events()
            dt = self.clock.tick(FPS) / 1000.0
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()
