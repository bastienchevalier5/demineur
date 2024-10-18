#   ___                      _                                             
#  |   \    ___    _ __     (_)    _ _      ___    _  _      _ _     o O O 
#  | |) |  / -_)  | '  \    | |   | ' \    / -_)  | +| |    | '_|   o      
#  |___/   \___|  |_|_|_|  _|_|_  |_||_|   \___|   \_,_|   _|_|_   TS__[O] 
#_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| {======| 
#"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000' 

# Démineur en Python

Bienvenue dans le projet **Démineur** ! Ce jeu classique vous plonge dans un défi de logique où vous devez éviter les mines cachées sur un plateau. Le but du jeu est de révéler toutes les cases qui ne contiennent pas de mines tout en marquant correctement les mines.

## Table des matières

- [Installation](#installation)
- [Lancer le projet](#lancer-le-projet)
- [À quoi sert ce projet ?](#à-quoi-sert-ce-projet-)
- [Options de jeu](#options-de-jeu)
- [Contribuer](#contribuer)
- [Auteurs](#auteurs)
- [Licence](#licence)

## Installation

Pour exécuter ce projet, vous devez avoir Python installé sur votre machine. Voici comment procéder :

1. **Installer Python** :
   - Téléchargez la dernière version de Python sur le site officiel : [python.org](https://www.python.org/downloads/).
   - Suivez les instructions d'installation et assurez-vous de cocher l'option pour ajouter Python à votre PATH.

2. **Cloner le projet** :
   Ouvrez un terminal et exécutez la commande suivante pour cloner le dépôt :
   ```bash
   git clone https://github.com/bastienchevalier5/demineur
Remplacez username par votre nom d'utilisateur GitHub.

Naviguer dans le répertoire du projet :

bash
Copier le code
cd demineur
Installer les dépendances (si nécessaire) : Si votre projet a des dépendances supplémentaires, vous pouvez les installer via pip. Par exemple :

bash
Copier le code
pip install -r requirements.txt
Note : Ce projet n'a pas de dépendances externes spécifiques au-delà de Python standard.

Lancer le projet
Pour lancer le jeu, exécutez simplement le script Python :

bash
Copier le code
python demineur.py
À quoi sert ce projet ?
Ce projet est une implémentation du jeu classique Démineur (Minesweeper) en Python utilisant la bibliothèque Tkinter pour l'interface graphique. Le jeu vous propose de :

Éviter les mines cachées.
Utiliser la logique pour déduire la position des mines en révélant les cases.
Marquer les mines avec des drapeaux pour éviter de cliquer dessus par erreur.
Options de jeu
Le jeu propose plusieurs options pour améliorer l'expérience :

Niveaux de difficulté :

Facile (8x8, 10 mines)
Moyen (12x12, 20 mines)
Difficile (16x16, 40 mines)
Mode triche :

Vous pouvez activer le mode triche en cliquant sur le titre du jeu, ce qui révélera la position de toutes les mines.

Chronomètre :

Un chronomètre en haut de l'écran suit le temps écoulé depuis le début de la partie.
Compteur de mines :

Un compteur affichant le nombre de mines restantes à marquer.
