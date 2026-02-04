"""
╔════════════════════════════════════════════════════════════════╗
║           DOCUMENTATION - STRUCTURE DU JEUX                   ║
╚════════════════════════════════════════════════════════════════╝

📁 STRUCTURE DES FICHIERS
════════════════════════════════════════════════════════════════

src/
├── __init__.py              # Package Python vide
├── configuration.py         # Constantes et paramètres du jeu
├── jeu.py                   # Boucle principale et gestion d'états
├── etapes.py                # Logique des deux phases (QTE + Arrow Rush)
├── ressources.py            # Gestion des sprites et images
├── utilitaires.py           # Fonctions helper (texte, barres, images)
├── notification.py          # Popups de feedback (PERFECT! / MISS!)
└── popup.py                 # (Ancien - à supprimer)

main.py                       # Point d'entrée du jeu

════════════════════════════════════════════════════════════════

📚 DESCRIPTION DES MODULES
════════════════════════════════════════════════════════════════

1️⃣  MAIN.PY - Point d'entrée
   └─ Lance le jeu en créant une instance de la classe Jeu
   └─ Exécute la boucle principale avec jeu.executer()

2️⃣  CONFIGURATION.PY - Paramètres centralisés
   └─ Dimensions écran, FPS
   └─ Chemins des ressources (images)
   └─ Constantes Phase 1 (QTE):
      • Nombre de défis: 6
      • Rayon zone clic: 50 pixels
      • Temps par défi: 2 secondes
   └─ Constantes Phase 2 (Arrow Rush):
      • Nombre de flèches: 25
      • Vitesse de chute: 250 px/s
      • Fenêtre de hit: 50 pixels (tolérance)
      • Contrôles AZERTY: Z/Q/S/D
   └─ Points de vie:
      • Joueur: 10 PV
      • Boss: 100 PV
   └─ Dégâts:
      • Hit QTE: -20 PV boss
      • Miss QTE: -1 PV joueur
      • Hit Flèche: -5 PV boss
      • Miss Flèche: 0 PV joueur (pas de punition)
   └─ Palette de couleurs

3️⃣  JEU.PY - Moteur du jeu
   └─ Classe Jeu: Gère la boucle principale
      • __init__(): Initialise Pygame et les ressources
      • traiter_evenements(): Capture une seule touche par frame
      • actualiser(dt): Met à jour la logique selon la phase
      • dessiner(): Affiche l'interface
      • executer(): Boucle infinie (60 FPS)
   └─ États du jeu:
      • "menu": Écran titre
      • "qte_phase1": Phase 1 QTE
      • "fleches_phase2": Phase 2 Arrow Rush
      • "victoire": Écran victoire
      • "defaite": Écran défaite

4️⃣  ÉTAPES.PY - Logique des phases
   └─ DefiQTE: Phase 1
      • Génère une cible circulaire aléatoire
      • Affiche une touche à appuyer
      • Détecte si le joueur clic au bon moment
      • Affiche notification (PERFECT! / MISS!)
      • 6 défis à compléter pour progresser
   
   └─ ConcoursFlèches: Phase 2
      • Génère des flèches tombantes au rythme
      • Joueur doit appuyer Z/Q/S/D au bon moment
      • Ghost zones orange montrent la fenêtre de hit (50px)
      • 25 flèches à frapper pour terminer
      • Système de combo
      • Textes flottants (+5 DMG)

5️⃣  RESSOURCES.PY - Gestion visuelle
   └─ Classe Ressources: Charge les sprites
      • Charge le fond d'écran
      • Charge le joueur, boss, anneau
      • Redimensionne à la taille appropriée
      • Gère la transparence (convert_alpha)

6️⃣  UTILITAIRES.PY - Helpers
   └─ charger_image(chemin): Charge une image avec gestion d'erreur
   └─ dessiner_texte(surface, texte, taille, x, y, couleur, gras):
      Affiche du texte centré
   └─ dessiner_barre(surface, x, y, largeur, hauteur, fraction, ...):
      Affiche une barre de vie/progression

7️⃣  NOTIFICATION.PY - Popups de feedback
   └─ NotificationRésultat: Popup style MMA
      • Affiche "PERFECT! +5 DMG" en vert (succès)
      • Affiche "MISS! COMBO x0" en rouge (échec)
      • Effets de fade-out et shake
      • Durée: ~0.33 secondes

════════════════════════════════════════════════════════════════

🎮 FLUX DU JEU
════════════════════════════════════════════════════════════════

START
  ↓
main.py → Crée Jeu()
  ↓
jeu.executer() → Boucle 60 FPS
  ↓
traiter_evenements() → Capture les touches (1 seule/frame)
  ↓
actualiser(dt) → Met à jour la logique
  ├─ Si "qte_phase1":
  │   └─ DefiQTE.actualiser()
  │   └─ Résultat: hit / miss / complete
  │   └─ Affiche notification popup
  │
  └─ Si "fleches_phase2":
      └─ ConcoursFlèches.actualiser()
      └─ Résultat: hit / miss / complete
      └─ Affiche notification popup
  ↓
dessiner() → Affiche l'interface
  ├─ Fond, boss, joueur
  ├─ Barres de vie
  ├─ Phase actuelle (menu / QTE / Arrow / Win / Lose)
  └─ Notifications
  ↓
pygame.display.flip() → Rafraîchit l'écran

════════════════════════════════════════════════════════════════

🔧 TRANSITIONS
════════════════════════════════════════════════════════════════

Menu → QTE Phase 1
  ├─ Toucher ENTRÉE
  ├─ État = "qte_phase1"
  └─ DefiQTE() créé

QTE Phase 1 → Arrow Phase 2
  ├─ Compléter 6 défis
  ├─ État = "fleches_phase2"
  ├─ Régénère PV joueur et boss
  └─ ConcoursFlèches() créé

Arrow Phase 2 → Victoire/Défaite
  ├─ Si 25 flèches frappées: Victoire
  ├─ Si PV joueur = 0: Défaite
  └─ État = "victoire" ou "defaite"

Victoire/Défaite → Menu
  ├─ Toucher R
  ├─ reinitialiser()
  └─ État = "menu"

════════════════════════════════════════════════════════════════

📊 POINTS DE VIE ET DÉGÂTS
════════════════════════════════════════════════════════════════

Phase 1 (QTE):
  Boss: 100 PV
    ├─ -20 par hit (6 max = 120 dégâts)
    └─ Régénère 100 PV avant phase 2
  
  Joueur: 10 PV
    ├─ -1 par miss (6 max perdre 6)
    └─ Régénère 10 PV avant phase 2

Phase 2 (Arrow Rush):
  Boss: 100 PV (réinitialisé)
    ├─ -5 par hit (25 max = 125 dégâts)
    └─ Défaite si = 0
  
  Joueur: 10 PV (réinitialisé)
    ├─ 0 PV par miss (pas de punition)
    └─ Défaite si = 0

════════════════════════════════════════════════════════════════

⌨️  CONTRÔLES
════════════════════════════════════════════════════════════════

Menu:
  ENTRÉE → Démarrer
  ECHAP  → Quitter

QTE Phase 1:
  Q/W/E/R/A/S/D/Z/X/C → Appuyer selon la touche affichée
  ECHAP                 → Quitter

Arrow Phase 2 (AZERTY):
  Z     → Flèche haut (bleu)
  Q     → Flèche gauche (orange)
  S     → Flèche bas (vert)
  D     → Flèche droite (jaune)
  ECHAP → Quitter

Victoire/Défaite:
  R     → Rejouer
  ECHAP → Quitter

════════════════════════════════════════════════════════════════

🎨 SYSTÈME DE FEEDBACK VISUEL
════════════════════════════════════════════════════════════════

Popup (NotificationRésultat):
  ✓ Succès: "PERFECT! +5 DMG" en vert
  ✗ Échec: "MISS! COMBO x0" en rouge
  - Animé avec shake (secousse)
  - Fade-out (disparition progressive)
  - Durée: ~0.33 secondes

Zones de hit (Ghost zones):
  - Orange pour Arrow Rush
  - ±50 pixels autour de la ligne cible
  - Aide le joueur à viser

Animations:
  ├─ Flash succès: Zone devient verte brièvement
  ├─ Flash échec: Zone devient rouge brièvement
  ├─ Brightness: Flèches brillent en approchant
  ├─ Textes flottants: "+5 DMG" monte et disparaît
  └─ Combo affiché en haut à gauche

════════════════════════════════════════════════════════════════

🔍 NOTES DE DÉVELOPPEMENT
════════════════════════════════════════════════════════════════

Touches simultanées (multi-touch):
  ✓ Fixé: Une seule touche par frame via événements
  ✗ Ancien: pygame.key.get_pressed() détectait tout simultanément

Performance:
  ✓ Pas de lag au démarrage (pas de spawn initial)
  ✓ Ghost zones réduits (50px au lieu de 70px)
  ✓ 60 FPS cible

À améliorer:
  - Animations plus fluides
  - Effets sonores
  - Difficultés multiples
  - Classement haut-scores

════════════════════════════════════════════════════════════════
"""
