# Easter Egg - Boss Fight 🎮

Mini-jeu de combat de boss avec deux phases de gameplay distinctes et challengeantes.

## 🚀 Lancement rapide

### Installation
```bash
# Installer les dépendances
pip install pygame
```

### Lancer le jeu
```bash
# Depuis le dossier du projet
python main.py
```

---

## 🎯 But du jeu

Affrontez un boss redoutable dans un combat en deux phases ! Gérez vos **10 PV** avec soin car chaque erreur vous coûte cher. Le boss commence avec **100 PV** et se régénère complètement entre les phases.

### 📍 Phase 1 : QTE (Quick Time Events)
**Objectif** : Réussir 6 défis de réflexes pour vaincre le boss

**Comment jouer** :
- Des cercles bleus apparaissent aléatoirement à l'écran
- Chaque cercle affiche une **touche** (Q, W, E, R, A, S, D, Z, X, C)
- Placez votre **souris dans le cercle** ET appuyez sur la **touche affichée**
- Vous avez **2 secondes** par QTE avant le timeout
- Barre de temps orange en bas pour suivre le chrono

**Scoring** :
- ✅ Succès : **-20 PV** au boss
- ❌ Échec : **-1 PV** pour vous

### 🎵 Phase 2 : Arrow Rush (Jeu de Rythme)
**Objectif** : Faire descendre la barre de vie du boss à 0 en 60 secondes!

**Comment jouer** :
- Des **flèches colorées** (↑ ← ↓ →) descendent du haut de l'écran
- Chaque flèche correspond à une touche : **W** (↑ bleu), **A** (← orange), **S** (↓ vert), **D** (→ jaune)
- Une **ligne blanche** marque la zone cible en bas
- Appuyez sur la **bonne touche** quand la flèche **atteint la ligne**
- Timing précis requis pour réussir !

**Difficulté progressive** :
- **Toujours** : 1 flèche à la fois - simple et amusant!

**Animations** :
- ✅ Succès : Zone verte + pulsation  
- ❌ Échec : Zone rouge + flash

**Scoring** :
- ✅ Succès : **-5 PV** au boss
- ❌ Miss : **-1 PV** pour vous

**Défi** : Tu as **60 secondes** pour vaincre le boss! Un minuteur s'affiche en haut à droite! ⏱️

---

## 🎮 Contrôles

| Touche | Action |
|--------|--------|
| **ENTRÉE** | Démarrer le jeu |
| **SOURIS + Touches** | Phase 1 - QTE |
| **W/A/S/D** | Phase 2 - Arrow Rush |
| **R** | Rejouer après victoire/défaite |
| **ÉCHAP** | Quitter |

---

## 📁 Structure du projet

```
easter egg/
├── main.py              # Point d'entrée du jeu
├── src/
│   ├── config.py        # Configuration et constantes
│   ├── game.py          # Boucle principale et logique
│   ├── stages.py        # Classes QTE et ArrowRush
│   ├── assets.py        # Gestion des sprites
│   └── utils.py         # Fonctions utilitaires
├── ring.png             # Background de l'arène
├── player.png           # Sprite du joueur
└── Combattant.png       # Sprite du boss
```

---

## 💡 Conseils de survie

- 🎯 **Phase 1** : Anticipez les cercles et préparez vos doigts sur les touches
- ⚡ **Phase 2** : Suivez l'aiguille des yeux et réagissez instinctivement
- 💚 **Gestion HP** : Chaque erreur compte - la précision vaut mieux que la vitesse!
- 🔥 **Boss régénéré** : Ne vous découragez pas quand il retrouve 100 PV en phase 2

Bonne chance, vous en aurez besoin! 🍀
