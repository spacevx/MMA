"""
════════════════════════════════════════════════════════════════
  MODULE ÉTAPES - Logique des phases de jeu
════════════════════════════════════════════════════════════════
Contient les deux phases du jeu:
- Phase 1 (DefiQTE): Quick Time Events
- Phase 2 (ConcoursFlèches): Arrow Rush (jeu de rythme)
"""
import math
import random
import pygame
from .configuration import (
    RAYON_QTE, LIMITE_TEMPS_QTE, TOUCHES_QTE, NOMBRE_DEFIS_QTE,
    NOMBRE_FLECHES_TOTAL, VITESSE_CHUTE_FLECHES, INTERVALLE_SPAWN, 
    POSITION_Y_CIBLE, FENETRE_HIT, TAILLE_FLECHE, TOUCHES_FLECHES,
    SEUIL_DIFFICULTE_2, SEUIL_DIFFICULTE_3, DUREE_JEU_FLECHES,
    GRACE_MANQUE,
    BLEU, JAUNE, ROUGE, VERT, NOIR, BLANC, ORANGE, GRIS
)
from .utilitaires import dessiner_texte
from .notification import NotificationRésultat


class DefiQTE:
    """
    Phase 1: Quick Time Events.
    Le joueur doit cliquer au bon moment dans une zone circulaire
    avec la bonne touche affichée.
    """

    def __init__(self, largeur_ecran, hauteur_ecran):
        """Initialiser la phase QTE."""
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.effectue = 0
        self.total = NOMBRE_DEFIS_QTE
        self.notification = NotificationRésultat()  # Popup style MMA
        self._reinitialiser_cible()

    def _reinitialiser_cible(self):
        """Générer une nouvelle cible aléatoire avec touche."""
        marge = 150
        self.x = random.randint(marge, self.largeur_ecran - marge)
        self.y = random.randint(150, self.hauteur_ecran - 150)
        self.touche = random.choice(TOUCHES_QTE)
        self.minuteur = LIMITE_TEMPS_QTE

    def actualiser(self, dt, pos_souris, touche_appuyee):
        """
        Mettre à jour la logique du QTE.
        - dt: Delta temps en secondes
        - pos_souris: Position (x, y) de la souris
        - touche_appuyee: Touche appuyée (key_code pygame)
        Retourne: "hit" (succès), "miss" (échec), "complete" (phase terminée) ou None
        """
        self.minuteur -= dt
        self.notification.actualiser()
        
        # Timeout - le temps a expiré
        if self.minuteur <= 0:
            self.notification.afficher("echec")
            self._reinitialiser_cible()
            return "miss"
        
        # Vérifier si la touche correcte a été appuyée
        if touche_appuyee == self.touche:
            mx, my = pos_souris
            distance = math.hypot(mx - self.x, my - self.y)
            if distance <= RAYON_QTE:
                # Succès!
                self.notification.afficher("succes")
                self.effectue += 1
                if self.effectue >= self.total:
                    return "complete"
                self._reinitialiser_cible()
                return "hit"
            else:
                # Mauvaise position
                self.notification.afficher("echec")
                self._reinitialiser_cible()
                return "miss"
        
        return None

    def dessiner(self, surface):
        """
        Afficher le QTE avec la zone cible, la touche et le timer.
        """
        # Cercle bleu (zone de clic)
        pygame.draw.circle(surface, BLEU, (self.x, self.y), RAYON_QTE, 3)
        
        # Cercle jaune intérieur (indicateur du centre)
        pygame.draw.circle(surface, JAUNE, (self.x, self.y), RAYON_QTE // 2, 2)
        
        # Texte de la touche à appuyer
        texte_touche = pygame.key.name(self.touche).upper()
        police = pygame.font.Font(None, 28)
        surface_texte = police.render(texte_touche, True, NOIR)
        rect_texte = surface_texte.get_rect(center=(self.x, self.y))
        
        # Fond blanc derrière le texte pour visibilité
        pygame.draw.rect(surface, BLANC, rect_texte.inflate(12, 8), border_radius=4)
        pygame.draw.rect(surface, NOIR, rect_texte.inflate(12, 8), 1, border_radius=4)
        surface.blit(surface_texte, rect_texte)
        
        # Afficher la notification (popup success/fail)
        self.notification.dessiner(surface)


class ConcoursFlèches:
    """
    Phase 2: Arrow Rush.
    Un jeu de rythme où les flèches tombent et le joueur doit
    appuyer sur les touches correspondantes au bon moment.
    Utilise les touches AZERTY: Z/Q/S/D
    """

    def __init__(self):
        """Initialiser la phase Arrow Rush."""
        self.effectue = 0
        self.total = NOMBRE_FLECHES_TOTAL
        self.fleches = []
        self.minuteur_spawn = 0.0
        self.temps_ecoule = 0.0
        self.duree_jeu = DUREE_JEU_FLECHES
        self.effets_retour = {}  # Flash de feedback sur les zones
        self.combo = 0
        self.textes_flottants = []  # Notifications flottantes (+5 DMG)
        self.cooldown_manque = 0.0  # Évite trop de dégâts d'affilée
        self.notification = NotificationRésultat()  # Popup style MMA
        # Pas de spawn initial - évite les lags au démarrage

    def _obtenir_multiplicateur_difficulte(self):
        """
        Retourner le multiplicateur de difficulté en fonction du progrès.
        Plus le joueur progresse, plus c'est difficile.
        """
        if self.effectue == 0:
            return 1
        ratio_succes = self.effectue / self.total
        if ratio_succes >= SEUIL_DIFFICULTE_3:
            return 3
        elif ratio_succes >= SEUIL_DIFFICULTE_2:
            return 2
        return 1

    def generer_fleche(self):
        """Créer une nouvelle flèche qui tombera."""
        if len(self.fleches) < 20:
            # Pour l'instant: seulement des flèches simples (1 touche)
            touche_selectionnee = random.choice(list(TOUCHES_FLECHES.keys()))
            
            self.fleches.append({
                'touches': [touche_selectionnee],
                'y': -50,
                'frappee': False
            })

    def actualiser(self, dt, touche_appuyee_cette_frame):
        """
        Mettre à jour la logique du Arrow Rush.
        - dt: Delta temps en secondes
        - touche_appuyee_cette_frame: Touche appuyée (key_code pygame, UNE SEULE par frame)
        Retourne: "hit" (succès), "miss" (échec), "complete" (phase terminée) ou None
        """
        self.temps_ecoule += dt
        
        # Mettre à jour la notification
        self.notification.actualiser()
        
        # Gérer le cooldown pour éviter les dégâts répétitifs
        if self.cooldown_manque > 0:
            self.cooldown_manque = max(0.0, self.cooldown_manque - dt)
        
        # Spawn de nouvelles flèches au rythme
        self.minuteur_spawn += dt
        if self.minuteur_spawn >= INTERVALLE_SPAWN:
            self.generer_fleche()
            self.minuteur_spawn = 0.0
        
        # Mettre à jour les positions des flèches
        for fleche in self.fleches[:]:
            if not fleche['frappee']:
                fleche['y'] += VITESSE_CHUTE_FLECHES * dt
            
            # Supprimer les flèches qui ont dépassé l'écran
            if fleche['y'] > POSITION_Y_CIBLE + FENETRE_HIT + GRACE_MANQUE:
                self.fleches.remove(fleche)
                if not fleche['frappee']:
                    # Flèche manquée - réinitialiser le combo
                    self.combo = 0
        
        # Mettre à jour les textes flottants (+5 DMG)
        for texte in self.textes_flottants[:]:
            texte['temps'] += dt
            texte['y'] -= 60 * dt  # Montée vers le haut
            if texte['temps'] >= texte['temps_max']:
                self.textes_flottants.remove(texte)
        
        # Diminuer les effets de feedback progressivement
        for touche in list(self.effets_retour.keys()):
            self.effets_retour[touche] -= dt
            if self.effets_retour[touche] <= 0:
                del self.effets_retour[touche]
        
        # Détection des touches - UNE SEULE par frame (via événement)
        if touche_appuyee_cette_frame is not None:
            # Mapper les codes pygame aux touches AZERTY
            correspondance_touches = {
                pygame.K_z: 'Z',
                pygame.K_q: 'Q',
                pygame.K_s: 'S',
                pygame.K_d: 'D'
            }
            
            if touche_appuyee_cette_frame in correspondance_touches:
                touche = correspondance_touches[touche_appuyee_cette_frame]
                resultat = self._verifier_hit(touche)
                if resultat:
                    return resultat
        
        return None

    def _verifier_hit(self, touche_appuyee):
        """
        Vérifier si le joueur a appuyé au bon moment.
        Détecte les flèches valides dans la fenêtre de hit.
        """
        # Trouver les flèches correspondantes dans la fenêtre de hit
        fleches_valides = []
        for fleche in self.fleches:
            if touche_appuyee in fleche['touches'] and not fleche['frappee']:
                distance = abs(fleche['y'] - POSITION_Y_CIBLE)
                if distance <= FENETRE_HIT:
                    fleches_valides.append((distance, fleche))
        
        # Si des flèches valides sont trouvées
        if fleches_valides:
            # Prendre la plus proche
            fleches_valides.sort(key=lambda x: x[0])
            _, meilleure_fleche = fleches_valides[0]
            
            # Marquer toutes les touches comme frappées
            for touche in meilleure_fleche['touches']:
                self.effets_retour[touche] = 0.3
            
            # Afficher le popup de succès
            self.notification.afficher("succes")
            
            # Créer une notification flottante "+5 DMG"
            caractere_fleche, (pos_x_base, _), couleur_touche = TOUCHES_FLECHES[touche_appuyee]
            self.textes_flottants.append({
                'texte': '+5',
                'x': pos_x_base,
                'y': POSITION_Y_CIBLE - 50,
                'temps': 0.0,
                'temps_max': 0.6,
                'couleur': VERT
            })
            
            meilleure_fleche['frappee'] = True
            self.effectue += 1
            self.combo += 1
            
            if self.effectue >= self.total:
                return "complete"
            return "hit"
        
        # Mauvais timing - affuyer mais pas sur une flèche valide
        # Ne montrer le popup fail que si on est proche d'une zone
        distance_proche = float('inf')
        for fleche in self.fleches:
            if touche_appuyee in fleche['touches'] and not fleche['frappee']:
                distance = abs(fleche['y'] - POSITION_Y_CIBLE)
                if distance < distance_proche:
                    distance_proche = distance
        
        # Popup fail seulement si proche de la zone (zone élargie)
        if distance_proche < FENETRE_HIT * 1.5:
            self.effets_retour[touche_appuyee] = 0.2
            self.notification.afficher("echec")
            self.combo = 0
        
        return None

    def dessiner(self, surface, centre):
        """
        Afficher le jeu Arrow Rush avec les flèches, zones et effets.
        """
        # Zone cible (ligne horizontale blanche)
        pygame.draw.line(surface, BLANC, (300, POSITION_Y_CIBLE), (660, POSITION_Y_CIBLE), 4)
        pygame.draw.line(surface, JAUNE, (300, POSITION_Y_CIBLE - 2), (660, POSITION_Y_CIBLE - 2), 2)
        
        # Zones de hit (ghost zones en orange) pour chaque colonne
        for touche, (caractere_fleche, (pos_x, _), couleur_touche) in TOUCHES_FLECHES.items():
            # Dessiner la zone d'acceptation (ghost zone) en orange
            pos_top = POSITION_Y_CIBLE - FENETRE_HIT
            hauteur_zone = FENETRE_HIT * 2
            pygame.draw.rect(surface, ORANGE, (pos_x - 5, pos_top, TAILLE_FLECHE + 10, hauteur_zone), 1, border_radius=4)
            
            # Effet de flash lors du feedback (succès/échec)
            a_flash = touche in self.effets_retour
            if a_flash:
                alpha = int(200 * (self.effets_retour[touche] / 0.3))
                couleur_flash = VERT if self.effets_retour[touche] > 0.15 else ROUGE
                surface_flash = pygame.Surface((TAILLE_FLECHE + 20, 80), pygame.SRCALPHA)
                pygame.draw.rect(surface_flash, (*couleur_flash, alpha), (0, 0, TAILLE_FLECHE + 20, 80), border_radius=8)
                surface.blit(surface_flash, (pos_x - 10, POSITION_Y_CIBLE - 40))
            
            # Zone de réception avec animation
            couleur_bordure = couleur_touche
            epaisseur_bordure = 3
            if a_flash:
                pulse = 1.0 + 0.3 * (self.effets_retour[touche] / 0.3)
                epaisseur_bordure = max(2, int(3 * pulse))
                couleur_bordure = VERT if self.effets_retour[touche] > 0.15 else ROUGE
            
            pygame.draw.rect(surface, couleur_bordure, (pos_x, POSITION_Y_CIBLE - 25, TAILLE_FLECHE, TAILLE_FLECHE), epaisseur_bordure, border_radius=5)
            dessiner_texte(surface, touche, 18, pos_x + TAILLE_FLECHE // 2, POSITION_Y_CIBLE + 60, couleur_touche, gras=True)
        
        # Dessiner les flèches qui tombent
        for fleche in self.fleches:
            if fleche['frappee']:
                continue  # Ne pas afficher les flèches déjà frappées
            
            # Boucler sur chaque touche de la flèche
            for idx, touche in enumerate(fleche['touches']):
                caractere_fleche, (pos_x_base, _), couleur_touche = TOUCHES_FLECHES[touche]
                
                # Décalage horizontal si plusieurs touches
                decalage_x = 0
                if len(fleche['touches']) == 2:
                    decalage_x = -25 if idx == 0 else 25
                elif len(fleche['touches']) == 3:
                    decalage_x = -25 if idx == 0 else (0 if idx == 1 else 25)
                
                pos_x = pos_x_base + decalage_x
                pos_y = fleche['y']
                
                # Effet de proximité (brille plus en approchant de la cible)
                distance_cible = abs(pos_y - POSITION_Y_CIBLE)
                if distance_cible < 60:
                    luminosite = 1.0 + (1.0 - distance_cible / 60) * 0.5
                    couleur_touche = tuple(min(255, int(c * luminosite)) for c in couleur_touche)
                
                # Dessiner le carré de la flèche
                pygame.draw.rect(surface, couleur_touche, (pos_x, pos_y, TAILLE_FLECHE, TAILLE_FLECHE), border_radius=5)
                pygame.draw.rect(surface, BLANC, (pos_x, pos_y, TAILLE_FLECHE, TAILLE_FLECHE), 2, border_radius=5)
                dessiner_texte(surface, caractere_fleche, 32, pos_x + TAILLE_FLECHE // 2, pos_y + TAILLE_FLECHE // 2, NOIR, gras=True)
        
        # Instructions et statistiques
        dessiner_texte(surface, "Appuie sur Z/Q/S/D quand les flèches atteignent la zone!", 16, 480, 100, BLANC)
        dessiner_texte(surface, f"Combo: {self.combo}", 18, 50, 50, JAUNE, gras=True)
        
        # Dessiner les textes flottants (+5 DMG)
        for objet_texte in self.textes_flottants:
            progression = objet_texte['temps'] / objet_texte['temps_max']
            transparence = int(255 * (1 - progression))  # Disparait progressivement
            
            # Créer la surface texte
            police = pygame.font.Font(None, 48)
            surface_texte = police.render(objet_texte['texte'], True, objet_texte['couleur'])
            
            # Ajouter la transparence
            surface_texte.set_alpha(transparence)
            
            # Afficher
            rect_texte = surface_texte.get_rect(center=(objet_texte['x'], int(objet_texte['y'])))
            surface.blit(surface_texte, rect_texte)
        
        # Afficher la notification au-dessus de tout
        self.notification.dessiner(surface)
