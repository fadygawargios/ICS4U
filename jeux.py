
#  Description: Dans Énigme Nationale, l'élève de la 3e à la 4e année devra choisir 
#  le nom d'un pays parmi trois choix à partir d'une carte mondiale ou d'un drapeau pour atteindre
#  une certain montant de point. 

from common import * 
from PIL import Image
from random import randint
from fonctions import PoseMultiple, FermeImage, ObtenirOptions, listeHasard, formatList, PoseText, mergeSort
import time


# TODO: POP ALREADY SEEN QUESTIONS FROM THE LIST OF CARTES AND DREAPEAUX (to avoid repeats)
def ÉnigmeNationale(stdscr, objectif, écran_retroaction):
  # TODO: FIND A SPOT TO PUT THIS
  WHITE_AND_RED = curses.color_pair(2)
  WHITE_AND_GREEN = curses.color_pair(3)
  
  stdscr.nodelay(False)
  stdscr.clear()
  stdscr.addstr(1, 0, "Vous allez jouer Énigme Nationale!!")
  stdscr.addstr(2, 0, "Dans ce jeu, vous allez devoir identifier le nom d'un pays à partir d'un drapeau ou d'une carte mondiale.")
  stdscr.addstr(3, 0, "Cliquer ENTER pour commencer")
  stdscr.refresh()
  stdscr.getch()
  
  # Définit les points à 0
  points = 0

  # Montant d'erreurs que l'utulisateur a fait
  erreurs = 0

  # Lorsque l'utulisateur n'a pas atteint l'objectif de point
  while points != objectif:

    # Si le pointage est paire
    if points % 2 == 0:
      # Cherche les pays, leurs nom de fichers correspondante et la bonne response pour une question de drapeaux
      options, option_noms_fichier, index_bonne_réponse = ObtenirOptions(LISTE_DRAPEAUX)
      # Prépare la question
      question = "À quelle pays appartient ce drapeaux?"
      # Prépare le chemin de l'image de la bonne réponse
      chemin_image = os.path.join(CHEMIN_DRAPEAUX, option_noms_fichier[index_bonne_réponse])

    # Si le pointage est impaire
    else:
      # Cherche les pays, nom de ficher, et bonne réponse pour une question de cartes
      options, option_noms_fichier, index_bonne_réponse = ObtenirOptions(LISTE_CARTES)
      # Prépare le chemin de l'image de la bonne réponse
      chemin_image = os.path.join(CHEMIN_CARTES , option_noms_fichier[index_bonne_réponse])

    # Affiche l'image de la bonne réponse
    image = Image.open(str(chemin_image))
    image.show()

    # Obtient la réponse de l'utilisateur à la question
    réponse = PoseMultiple(stdscr, options, question)

    # Ferme l'image (pour qu'ils ne s'accumulent pas)
    FermeImage()


    # Si la réponse de l'utilisateur est la bonne réponse
    if réponse == options[index_bonne_réponse]:
      # Ajoute un point
      points += 1 

      # Imprime la rétroaction sur le window «écran_retroaction»
      écran_retroaction.clear()
      écran_retroaction.addstr(f"Bonne Réponse! Bravo!", WHITE_AND_GREEN | curses.A_BOLD)
      écran_retroaction.refresh()

    else:
      # Si l'utulisateur n'est pas à 0 points
      if points != 0:
        # Enleve un point
        points -= 1
      erreurs += 1
      
      # Imprime la rétroaction sur le window «écran_retroaction»
      écran_retroaction.clear()
      écran_retroaction.addstr(f"Mauvaise Réponse! La réponse était {options[index_bonne_réponse]}.", WHITE_AND_RED | curses.A_BOLD)
      écran_retroaction.refresh()
  
    # Affiche les changements de points
    écran_retroaction.addstr(1, 0, f"Points: {points}")
    écran_retroaction.refresh()

  return erreurs

#  Description: Dans YYY, l'élève de la 1e à la 2e devra

def PingouinsDuTri(stdscr, objectif, écran_retroaction):

  stdscr.clear()
  stdscr.addstr("Salut ..., vous allez jouer à ....")
  stdscr.refresh()
  stdscr.getch()
  liste_nonTriée = listeHasard(longeur=5, min=0, max=10)
  stdscr.clear()
  # TODO: Function to format str
  question = "Met la suite de nombre suivante en ordre croissant: " + formatList(liste_nonTriée)
  réponse = PoseText(stdscr, question)
  liste_triée = mergeSort(liste_nonTriée)
  stdscr.refresh()