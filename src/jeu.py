"""
════════════════════════════════════════════════════════════════
  MODULE JEU - Gestion principale de la boucle de jeu
════════════════════════════════════════════════════════════════
"""
import sys
import pygame
from .configuration import *
from .etapes import DefiQTE, ConcoursFlèches
from .ressources import Ressources
from .utilitaires import dessiner_texte, dessiner_barre


class Jeu:
    """Classe principale qui gère la boucle de jeu et les états."""
    
    def __init__(self):
        """Initialiser Pygame et les éléments du jeu."""
        pygame.init()
        pygame.display.set_caption("Easter Egg - Boss Fight")
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        self.horloge = pygame.time.Clock()
        self.ressources = Ressources()
        
        # Positions des personnages
        self.centre_anneau = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)
        self.pos_joueur = (LARGEUR_ECRAN - 100, HAUTEUR_ECRAN // 2 + 50)
        self.pos_boss = (100, HAUTEUR_ECRAN // 2 + 50)
        self.touche_appuyee_cette_frame = None  # Stocke UNE SEULE touche par frame
        
        self.reinitialiser()

    def reinitialiser(self):
        """Réinitialiser une partie."""
        self.etape = "menu"
        self._initialiser_etat_commun()
        self._demarrer_phase_qte()

    def _initialiser_etat_commun(self):
        """Réinitialiser les variables communes à toutes les phases."""
        self.pv_joueur = POINTS_VIE_JOUEUR
        self.pv_boss = POINTS_VIE_BOSS
        self.message = ""
        self.temps_message = 0.0

    def _demarrer_phase_qte(self):
        """Initialiser la Phase 1 (QTE)."""
        self.defi_qte = DefiQTE(LARGEUR_ECRAN, HAUTEUR_ECRAN)

    def _demarrer_phase_fleches(self):
        """Initialiser la Phase 2 (Arrow Rush)."""
        self.concours_fleches = ConcoursFlèches()

    def traiter_evenements(self):
        """Gérer les entrées utilisateur et événements."""
        self.touche_appuyee_cette_frame = None  # Réinitialiser à chaque frame
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return False
                if evenement.key == pygame.K_RETURN and self.etape == "menu":
                    self.etape = "qte_phase1"
                if evenement.key == pygame.K_r and self.etape in ("victoire", "defaite"):
                    self.reinitialiser()
                # Capturer UNE SEULE touche par frame pour éviter les multiples simultanées
                if self.touche_appuyee_cette_frame is None and evenement.key in [pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.touche_appuyee_cette_frame = evenement.key
        return True

    def actualiser(self, dt):
        """Mettre à jour la logique du jeu."""
        self.temps_message -= dt
        
        if self.etape == "qte_phase1":
            # Gérer la phase QTE
            resultat = self.defi_qte.actualiser(dt, pygame.mouse.get_pos(), self.obtenir_touche_appuyee())
            
            if resultat == "hit":
                self.pv_boss -= DEGATS_HIT_QTE
                self.message = "✓ Touché!"
                self.temps_message = 0.3
            elif resultat == "miss":
                self.pv_joueur -= DEGATS_MANQUE_QTE
                self.message = "✗ Manqué!"
                self.temps_message = 0.3
            elif resultat == "complete":
                # Régénère le boss ET le joueur pour la phase 2
                self.pv_boss = POINTS_VIE_BOSS
                self.pv_joueur = POINTS_VIE_JOUEUR
                self.etape = "fleches_phase2"
                self._demarrer_phase_fleches()
                self.message = ""
            
            if self.pv_joueur <= 0:
                self.etape = "defaite"
                self.message = ""
        
        elif self.etape == "fleches_phase2":
            # Gérer la phase Arrow Rush
            resultat = self.concours_fleches.actualiser(dt, self.touche_appuyee_cette_frame)
            
            if resultat == "hit":
                self.pv_boss -= DEGATS_HIT_FLECHES
                self.message = "🎯 Hit!"
                self.temps_message = 0.3
            elif resultat == "miss":
                self.pv_joueur -= DEGATS_MANQUE_FLECHES
                self.message = "✗ Miss!"
                self.temps_message = 0.3
            elif resultat == "complete":
                self.etape = "victoire"
                self.message = ""
            
            if self.pv_joueur <= 0:
                self.etape = "defaite"
                self.message = ""
            
            if self.pv_boss <= 0:
                self.etape = "victoire"
                self.message = ""

    def obtenir_touche_appuyee(self):
        """Retourner la touche appuyée actuellement (pour QTE)."""
        touches = pygame.key.get_pressed()
        for touche in TOUCHES_QTE:
            if touches[touche]:
                return touche
        return None

    def dessiner(self):
        """Dessiner tous les éléments de l'interface."""
        self.ressources.dessiner_fond(self.ecran)
        self.ressources.dessiner_anneau(self.ecran, self.centre_anneau)
        self.ressources.dessiner_boss(self.ecran, self.pos_boss)
        self.ressources.dessiner_joueur(self.ecran, self.pos_joueur)
        
        # Barres de vie
        dessiner_barre(self.ecran, 20, HAUTEUR_ECRAN - 60, 180, 14, self.pv_boss / POINTS_VIE_BOSS, ROUGE, GRIS)
        dessiner_texte(self.ecran, "Boss", 14, 20, HAUTEUR_ECRAN - 42, BLANC)
        
        dessiner_barre(self.ecran, LARGEUR_ECRAN - 200, HAUTEUR_ECRAN - 60, 180, 14, self.pv_joueur / POINTS_VIE_JOUEUR, VERT, GRIS)
        dessiner_texte(self.ecran, "Joueur", 14, LARGEUR_ECRAN - 200, HAUTEUR_ECRAN - 42, BLANC)
        
        # Affichage selon la phase/état
        if self.etape == "menu":
            dessiner_texte(self.ecran, "BOSS FIGHT", 48, LARGEUR_ECRAN // 2, 100, JAUNE)
            dessiner_texte(self.ecran, "Phase 1: QTE | Phase 2: Arrow Rush", 20, LARGEUR_ECRAN // 2, 160, BLANC)
            dessiner_texte(self.ecran, "Appuie sur ENTRÉE", 18, LARGEUR_ECRAN // 2, 220, ORANGE)
        
        elif self.etape == "qte_phase1":
            dessiner_texte(self.ecran, f"QTE Phase 1 ({self.defi_qte.effectue}/{self.defi_qte.total})", 20, 20, 20, BLANC)
            dessiner_texte(self.ecran, "Mets la souris dans le cercle et appuie sur la touche", 16, LARGEUR_ECRAN // 2, 50, BLANC)
            self.defi_qte.dessiner(self.ecran)
            
            # Barre de temps
            progression = self.defi_qte.minuteur / LIMITE_TEMPS_QTE
            dessiner_barre(self.ecran, LARGEUR_ECRAN // 2 - 100, HAUTEUR_ECRAN - 30, 200, 10, progression, ORANGE, GRIS)
        
        elif self.etape == "fleches_phase2":
            dessiner_texte(self.ecran, f"Arrow Rush ({self.concours_fleches.effectue}/{self.concours_fleches.total})", 20, 20, 20, BLANC)
            self.concours_fleches.dessiner(self.ecran, self.centre_anneau)
            
            # Barre de vie du boss
            dessiner_barre(self.ecran, 20, HAUTEUR_ECRAN - 60, 180, 14, self.pv_boss / POINTS_VIE_BOSS, ROUGE, GRIS)
            dessiner_texte(self.ecran, "Boss", 14, 20, HAUTEUR_ECRAN - 42, BLANC)
        
        elif self.etape == "victoire":
            dessiner_texte(self.ecran, "VICTOIRE!", 48, LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 - 40, JAUNE)
            dessiner_texte(self.ecran, "Easter Egg terminé!", 24, LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 + 20, VERT)
            dessiner_texte(self.ecran, "Appuie sur R pour rejouer", 16, LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 + 70, BLANC)
        
        elif self.etape == "defaite":
            dessiner_texte(self.ecran, "DÉFAITE", 48, LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 - 40, ROUGE)
            dessiner_texte(self.ecran, "Tu as perdu tous tes PV!", 24, LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 + 20, ROUGE)
            dessiner_texte(self.ecran, "Appuie sur R pour réessayer", 16, LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 + 70, BLANC)
        
        # Afficher le message temporaire
        if self.temps_message > 0:
            dessiner_texte(self.ecran, self.message, 22, LARGEUR_ECRAN // 2, 90, BLANC)
        
        pygame.display.flip()

    def executer(self):
        """Boucle principale du jeu."""
        en_cours = True
        while en_cours:
            en_cours = self.traiter_evenements()
            dt = self.horloge.tick(IMAGES_PAR_SECONDE) / 1000.0
            self.actualiser(dt)
            self.dessiner()
