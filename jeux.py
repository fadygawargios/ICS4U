
#  Description: Dans Énigme Nationale, l'élève de la 3e à la 4e année devra choisir 
#  le nom d'un pays parmi trois choix à partir d'une carte mondiale ou d'un drapeau pour atteindre
#  une certain montant de point. 

from common import * 
from PIL import Image
from random import randint
from fonctions import PoseMultiple, FermeImage, ObtenirOptions, listeHasard, formatList, PoseText, mergeSort, print_ascii_art, VérifieRéponse
import time
import curses


# todo: POP ALREADY SEEN QUESTIONS FROM THE LIST OF CARTES AND DREAPEAUX (to avoid repeats)
def ÉnigmeNationale(stdscr, objectif, écran_retroaction):

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

    # todo: add comments
    résultat = VérifieRéponse(réponse, options[index_bonne_réponse], écran_retroaction)
    
    if résultat == False:
      erreurs += 1

      if points != 0:
        points -= 1
    else:
      points += 1
    # Affiche les changements de points
    écran_retroaction.addstr(1, 0, f"Points: {points}")
    écran_retroaction.refresh()

  return erreurs


#  Description: Dans YYY, l'élève de la 1e à la 2e devra

# todo: add comments
def PingouinsDuTri(stdscr, objectif, écran_retroaction):

  stdscr.nodelay(False)
  WHITE_AND_YELLOW = curses.color_pair(1)

  stdscr.clear()
  stdscr.addstr(5, 50, "Salut ..., vous allez jouer à ")
  stdscr.addstr(5, 80, "PINGOINS DU TRI", WHITE_AND_YELLOW)
  print_ascii_art(stdscr)
  stdscr.refresh()
  stdscr.getch()

  points = 0 

  while points != objectif:
    liste_nonTriée = listeHasard(longeur=5, min=0, max=10)
    stdscr.clear()
    question = "Met la suite de nombre suivante en ordre croissant: " + formatList(liste_nonTriée)
    réponse = PoseText(stdscr, question)
    
    réponse_formatted = []
    
    for nombre in réponse:
      if nombre != "":
        réponse_formatted.append(int(nombre.replace(",", "")))

    liste_triée = mergeSort(liste_nonTriée)

    # todo: try to break this...what if you input chars or idkk
    résultat = VérifieRéponse(réponse_formatted, liste_triée, écran_retroaction)
    
    if résultat == False:
      erreurs += 1

      if points != 0:
        points -= 1
    else:
      points += 1
    # Affiche les changements de points
    écran_retroaction.addstr(1, 0, f"Points: {points}")
    écran_retroaction.refresh()
    time.sleep(1.5)
  