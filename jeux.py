
#  Description: Dans Énigme Nationale, l'élève de la 3e à la 4e année devra choisir 
#  le nom d'un pays parmi trois choix à partir d'une carte mondiale ou d'un drapeau pour atteindre
#  une certain montant de point. 

from common import * 
from PIL import Image
from random import randint
from fonctions import Démarrage, PoseQuestion, FermeImage, ObtenirOptions


def ÉnigmeNationale(stdscr, objectif, écran_retroaction):
  WHITE_AND_RED = curses.color_pair(2)
  WHITE_AND_GREEN = curses.color_pair(3)
  
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
    réponse = PoseQuestion(stdscr, options, question)

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

def PingouinsDuTri():
  return 5