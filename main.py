#-------------------------------------------------------------------------------
#  Nom: Fady Gawargios
#  Titre: Jeux Éducatif
#  Description: Dans Énigme Nationale, l'élève de la 3e à la 4e année devra choisir 
#  le nom d'un pays parmi trois choix à partir d'une carte mondiale ou d'un drapeau pour atteindre
#  une certain montant de point. 
#--------------------------------------------------------------------------------

# Voir requirements.txt, un service de pipreqs (pip install pipreqs) pour installer toutes les dépendances du projet.
# Exécuter pip install -r requirements.txt pour installer les modules nécessaires. 

# *RAPPEL que le module curses ne fonctionnent pas dans votre line de commande, svp intaller git bash: https://git-scm.com/download/win


from fonctions import Démarrage, ÉcranFin
import curses
from jeux import ÉnigmeNationale, PingouinsDuTri
from common import * 

# stdscr -> «Standard Screen» que Curses va afficher au dessus du line de commande
def main(stdscr):
  
  # todo: make these french

  # Crée des paires de couleurs pour la ligne de commande
  # Paramètres: curses.init_pair(id, curses.COULEUR_TEXTE, curses.COULEUR_ARRIERE_PLAN)
  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_YELLOW)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

  # Appelle la fonction de démarrage pour choisir la difficulté
  # todo: make sure user put int for année 
  difficulté, nom, année = Démarrage(stdscr)

  # Établit l'objectif nécessaire en fonction de la difficulté choisie
  if difficulté == FACILE:
    objectif = 5
  elif difficulté == MOYENNE:
    objectif = 10
  else:
    objectif = 15

  # Crée un nouveau «window» au dessus de stdscr
  dimensions = stdscr.getmaxyx()
  largeur = dimensions[1]
  écran_retroaction = curses.newwin(10, largeur - 1, 6, 0)

  if année in [1, 2]:
    erreurs = PingouinsDuTri(stdscr, objectif, écran_retroaction)
  elif année in [3, 4]:
    erreurs = ÉnigmeNationale(stdscr, objectif, écran_retroaction)

    
  
  # Affiche l'écran de fin
  ÉcranFin(stdscr, erreurs, nom)
  


# Exécute la fonction principale avec Curses
curses.wrapper(main)