import os
import curses

# Définit les constantes de chemin
CHEMIN_DRAPEAUX = "./images/Drapeaux/"
CHEMIN_CARTES  = "images/Cartes/"

# Définit les constantes de difficulté
FACILE = 0
MOYENNE = 1
DIFFICILE = 2

# Obtient la liste de tous les fichiers dans les drapeaux et les cartes respectivement
LISTE_DRAPEAUX = os.listdir(CHEMIN_DRAPEAUX)
LISTE_CARTES  = os.listdir(CHEMIN_CARTES )
