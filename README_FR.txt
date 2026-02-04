"""
╔════════════════════════════════════════════════════════════════╗
║              EASTER EGG - BOSS FIGHT                          ║
║          Un mini-jeu à deux phases                            ║
║   Phase 1: Quick Time Events (QTE)                           ║
║   Phase 2: Arrow Rush (jeu de rythme)                        ║
╚════════════════════════════════════════════════════════════════╝

📖 GUIDE DE JEUX
════════════════════════════════════════════════════════════════

Le joueur affronte un boss sur deux phases:

PHASE 1: DÉFI QTE (Quick Time Events)
────────────────────────────────────────
- 6 défis à compléter
- Une cible circulaire bleu apparaît à l'écran
- Une touche est affichée au centre
- Vous devez:
  1. Placer la souris DANS le cercle
  2. Appuyer sur la touche affichée
  3. Avant que le temps (2 sec) ne soit écoulé
- Si réussi: Boss perd 20 PV
- Si échoué: Vous perdez 1 PV

PHASE 2: ARROW RUSH (Jeu de rythme)
────────────────────────────────────────
- 25 flèches à frapper
- Des carrés colorés tombent du haut
- Vous devez appuyer sur la bonne touche quand ils atteignent
  la ligne blanche horizontale
- Contrôles AZERTY:
  Z = Flèche haut (bleu)
  Q = Flèche gauche (orange)
  S = Flèche bas (vert)
  D = Flèche droite (jaune)
- Les zones orange montrent où appuyer (fenêtre de hit)
- Si réussi: Boss perd 5 PV
- Si échoué: Rien (-0 PV)

VICTOIRE / DÉFAITE
────────────────────────────────────
- Victoire: Frapper les 25 flèches de Phase 2
- Défaite: Perdre tous vos PV (10 PV)

════════════════════════════════════════════════════════════════

⚙️  INSTALLATION
════════════════════════════════════════════════════════════════

Prérequis:
  - Python 3.8+
  - Pygame 2.0+

Installation:
  1. Créer un environnement virtuel (optionnel):
     python -m venv .venv
     .venv\\Scripts\\Activate

  2. Installer Pygame:
     pip install pygame

  3. Lancer le jeu:
     python main.py

════════════════════════════════════════════════════════════════

📁 FICHIERS NÉCESSAIRES
════════════════════════════════════════════════════════════════

Images (dans le dossier racine):
  - ring.png          → Fond d'écran
  - player.png        → Sprite du joueur
  - Combattant.png    → Sprite du boss

Code Python:
  - main.py           → Point d'entrée
  - src/*.py          → Modules du jeu

════════════════════════════════════════════════════════════════

🎮 CONTRÔLES DÉTAILLÉS
════════════════════════════════════════════════════════════════

Écran d'accueil:
  [ENTRÉE]  → Démarrer le jeu
  [ECHAP]   → Quitter

Phase 1 (QTE):
  [Q, W, E, R, A, S, D, Z, X, C] → Appuyer selon la touche
  [ECHAP]                        → Quitter

Phase 2 (Arrow Rush):
  [Z]       → Flèche haut
  [Q]       → Flèche gauche
  [S]       → Flèche bas
  [D]       → Flèche droite
  [ECHAP]   → Quitter

Écran victoire/défaite:
  [R]       → Rejouer
  [ECHAP]   → Quitter

════════════════════════════════════════════════════════════════

🎯 ASTUCES DE JEU
════════════════════════════════════════════════════════════════

Phase 1:
  ✓ Restez concentré sur le minuteur (2 secondes)
  ✓ Lisez la touche correctement avant d'appuyer
  ✓ Vous pouvez repérer où la cible va apparaître

Phase 2:
  ✓ Régularité: Les flèches arrivent à intervalle constant
  ✓ Anticipation: Appuyez légèrement AVANT que la flèche
    ne atteigne la zone blanche
  ✓ Zones orange: Elles montrent exactement où appuyer
  ✓ Combo: Un indicateur en haut à gauche montre votre combo
  ✓ +5 DMG: Chaque hit affiche un "+5" flottant

════════════════════════════════════════════════════════════════

💾 FICHIER DE CONFIGURATION
════════════════════════════════════════════════════════════════

Tous les paramètres sont dans src/configuration.py:

Ajuster la difficulté:
  - NOMBRE_DEFIS_QTE: Nombre de challenges phase 1
  - FENETRE_HIT: Tolérance phase 2 (50px = difficile)
  - INTERVALLE_SPAWN: Vitesse des flèches
  - DEGATS_HIT_*: Dégâts infligés
  - POINTS_VIE_*: Points de vie

════════════════════════════════════════════════════════════════

📚 STRUCTURE DU CODE
════════════════════════════════════════════════════════════════

Voir DOCUMENTATION.md pour une description complète des modules.

Modules principaux:
  src/configuration.py  → Constantes du jeu
  src/jeu.py           → Boucle principale
  src/etapes.py        → Logique des phases
  src/ressources.py    → Gestion des images
  src/utilitaires.py   → Fonctions helper
  src/notification.py  → Popups de feedback

════════════════════════════════════════════════════════════════

🐛 TROUBLESHOOTING
════════════════════════════════════════════════════════════════

"Erreur: ring.png non trouvé"
  → Assurez-vous que les images sont dans le même dossier
     que main.py

"Le jeu lag"
  → Désactiver les appareils Bluetooth/USB inutiles
  → Fermer les autres applications lourdes

"Les touches ne répondent pas"
  → Vérifier le clavier (AZERTY / QWERTY)
  → Assurez-vous que la fenêtre du jeu a le focus

"Écran noir"
  → Vérifier que Pygame est installé: pip install pygame
  → Redémarrer le jeu

════════════════════════════════════════════════════════════════

📝 NOTES DE VERSION
════════════════════════════════════════════════════════════════

v1.0:
  ✓ Phase 1 complète (6 QTE)
  ✓ Phase 2 complète (25 flèches)
  ✓ Système de notification popup
  ✓ Contrôles AZERTY
  ✓ Pas de touches simultanées
  ✓ Ghost zones visibles
  ✓ Animations fluides

════════════════════════════════════════════════════════════════

Bon jeu! 🎮
"""
