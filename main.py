#-------------------------------------------------------------------------------
#  Nom: Fady Gawargios
#  Titre: Jeux Éducatif
#  Description: Ce fichier s'agit du «entry-point» dans un programme contenant deux jeux éducatif (Énigme Nationale et Pingouins du tri)
#  choisis en fonction de l'age de l'utulisateur. Durant chaque jeu, l'utulisateur devra atteindre un objectifs de points et recevera 
#  de la rétroaction si la réponse est mal. 
#--------------------------------------------------------------------------------

# Voir requirements.txt, un service de pipreqs (pip install pipreqs) pour installer toutes les dépendances du projet.
# Exécuter pip install -r requirements.txt pour installer les modules nécessaires. 

# *RAPPEL que le module curses ne fonctionnent pas dans votre line de commande, svp intaller git bash: https://git-scm.com/download/win

import curses
import common as c
from jeux import énigme_nationale, pingouins_du_tri
from fonctions import démarrage, écran_fin

# stdscr -> «Standard Screen» que Curses va afficher au dessus du line de commande
def main(stdscr):
  
  # Crée des paires de couleurs pour la ligne de commande
  # Paramètres: curses.init_pair(id, curses.COULEUR_TEXTE, curses.COULEUR_ARRIERE_PLAN)
  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_YELLOW)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

  # Appelle la fonction de démarrage pour choisir la difficulté
  difficulté, nom, année = démarrage(stdscr)

  # Établit l'objectif nécessaire en fonction de la difficulté choisie
  if difficulté == c.FACILE:
    objectif = 5
  elif difficulté == c.MOYENNE:
    objectif = 10
  else:
    objectif = 15

  # Crée un nouveau «window» au dessus de stdscr
  dimensions = stdscr.getmaxyx()
  largeur = dimensions[1]
  écran_retroaction = curses.newwin(10, largeur - 1, 6, 0)

  # Sélectionne le jeu correct en fonction de l'âge des utilisateurs
  if "1ère - 2ème année" in année:
    erreurs = pingouins_du_tri(stdscr, objectif, écran_retroaction)
  else:
    erreurs = énigme_nationale(stdscr, objectif, écran_retroaction)

  # Affiche l'écran de fin aprés la fin d'un des jeux
  écran_fin(stdscr, erreurs, nom)
  

# Exécute la fonction principale avec Curses
curses.wrapper(main)