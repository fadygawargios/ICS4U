from common import * 
from PIL import Image
from random import randint
from fonctions import PoseMultiple, FermeImage, ObtenirOptions, listeHasard, formatList, PoseText, mergeSort, print_ascii_art, VérifieRéponse
import time
import curses


def ÉnigmeNationale(stdscr, objectif, écran_retroaction):
  WHITE_AND_YELLOW = curses.color_pair(1)

  stdscr.nodelay(False)
  stdscr.clear()
  stdscr.addstr(4, 65, "BIENVENU À", curses.A_BOLD)
  stdscr.addstr(4, 65 + 11, "ÉNIGME NATIONALE!!", WHITE_AND_YELLOW | curses.A_BOLD)
  stdscr.addstr(5, 65, "Dans ce jeu, vous allez devoir identifier le nom")
  stdscr.addstr(6, 65, "d'un pays à partir d'un drapeau ou d'une carte mondiale.")
  stdscr.addstr(7, 65, "Cliquez sur n'importe quelle bouton pour commencer!")
  print_ascii_art(stdscr, jeu=1)
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
      question = f"QUESTION #{points + 1}: À quelle pays appartient ce drapeaux?"
      # Prépare le chemin de l'image de la bonne réponse
      chemin_image = os.path.join(CHEMIN_DRAPEAUX, option_noms_fichier[index_bonne_réponse])

    # Si le pointage est impaire
    else:
      # Cherche les pays, nom de ficher, et bonne réponse pour une question de cartes
      options, option_noms_fichier, index_bonne_réponse = ObtenirOptions(LISTE_CARTES)
      # Prépare la question
      question = f"QUESTION #{points + 1}: Quel est le pays sur la carte?"
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
  WHITE_AND_YELLOW = curses.color_pair(1)
  
  stdscr.nodelay(False)
  stdscr.clear()
  stdscr.addstr(5, 50, "BIENVENU À", curses.A_BOLD)
  stdscr.addstr(5, 61, "PINGOUINS DU TRI", WHITE_AND_YELLOW | curses.A_BOLD)
  stdscr.addstr(6, 50, "Dans ce jeu, vous allez devoir mettre des suites de")
  stdscr.addstr(7, 50, "nombres en ordre croissant et décroissant.")
  print_ascii_art(stdscr, jeu=2)
  stdscr.refresh()
  stdscr.getch()
  
  # Définit les points à 0
  points = 0

  # Montant d'erreurs que l'utulisateur a fait
  erreurs = 0

  # Lorsque l'utulisateur n'a pas atteint l'objectif de point
  while points != objectif:
    liste_nonTriée = listeHasard(longeur=5, min=1, max=100)
    stdscr.clear()
    if points % 2 == 0:
      question = f"QUESTION #{points + 1}: Met la suite de nombre suivante en ordre CROISSANT: " + formatList(liste_nonTriée)
      list_triée = mergeSort(liste_nonTriée, croissant=True)
    else:
      question = f"QUESTION #{points + 1}: Met la suite de nombre suivante en ordre DÉCROISSANT: " + formatList(liste_nonTriée)
      list_triée = mergeSort(liste_nonTriée, croissant=False)


    réponse = PoseText(stdscr, question)
    
    réponse_formatted = []
    
    for nombre in réponse:
      if nombre != "":
        réponse_formatted.append(int(nombre.replace(",", "")))

    

    # todo: try to break this...what if you input chars or idkk
    résultat = VérifieRéponse(réponse_formatted, list_triée, écran_retroaction)
    
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
  