from common import * 
from PIL import Image
from fonctions import pose_multiple, ferme_image, obtenir_options, liste_hasard, format_liste, pose_texte, merge_sort, imprime_art, vérifie_réponse, intro_jeu
import time

def énigme_nationale(stdscr, objectif, écran_retroaction):

  intro_jeu(stdscr, espace=65, jeu=1)
  
  # Définit les points à 0
  points = 0

  # Montant d'erreurs que l'utulisateur a fait
  erreurs = 0

  # Lorsque l'utulisateur n'a pas atteint l'objectif de point
  while points != objectif:

    # Si le pointage est paire
    if points % 2 == 0:
      # Cherche les pays, leurs nom de fichers correspondante et la bonne response pour une question de drapeaux
      options, option_noms_fichier, index_bonne_réponse = obtenir_options(LISTE_DRAPEAUX)
      # Prépare la question
      question = f"QUESTION #{points + 1}: À quelle pays appartient ce drapeaux?"
      # Prépare le chemin de l'image de la bonne réponse
      chemin_image = os.path.join(CHEMIN_DRAPEAUX, option_noms_fichier[index_bonne_réponse])

    # Si le pointage est impaire
    else:
      # Cherche les pays, nom de ficher, et bonne réponse pour une question de cartes
      options, option_noms_fichier, index_bonne_réponse = obtenir_options(LISTE_CARTES)
      # Prépare la question
      question = f"QUESTION #{points + 1}: Quel est le pays sur la carte?"
      # Prépare le chemin de l'image de la bonne réponse
      chemin_image = os.path.join(CHEMIN_CARTES , option_noms_fichier[index_bonne_réponse])

    # Affiche l'image de la bonne réponse
    image = Image.open(str(chemin_image))
    image.show()

    # Obtient la réponse de l'utilisateur à la question
    réponse = pose_multiple(stdscr, options, question)

    # Ferme l'image (pour qu'ils ne s'accumulent pas)
    ferme_image()

    # todo: add comments
    résultat = vérifie_réponse(réponse, options[index_bonne_réponse], écran_retroaction)
    
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
def pingouins_du_tri(stdscr, objectif, écran_retroaction):
  
  intro_jeu(stdscr, espace=50, jeu=2)
  
  # Définit les points à 0
  points = 0

  # Montant d'erreurs que l'utulisateur a fait
  erreurs = 0

  # Lorsque l'utulisateur n'a pas atteint l'objectif de point
  while points != objectif:
    liste_nonTriée = liste_hasard(longeur=5, min=1, max=100)
    stdscr.clear()
    if points % 2 == 0:
      question = f"QUESTION #{points + 1}: Met la suite de nombre suivante en ordre CROISSANT: " + format_liste(liste_nonTriée)
      list_triée = merge_sort(liste_nonTriée, croissant=True)
    else:
      question = f"QUESTION #{points + 1}: Met la suite de nombre suivante en ordre DÉCROISSANT: " + format_liste(liste_nonTriée)
      list_triée = merge_sort(liste_nonTriée, croissant=False)


    réponse = pose_texte(stdscr, question)
    
    réponse_formatted = []
    
    for nombre in réponse:
      if nombre != "":
        réponse_formatted.append(int(nombre.replace(",", "")))

    # todo: try to break this...what if you input chars or idkk
    résultat = vérifie_réponse(réponse_formatted, list_triée, écran_retroaction)
    
    if résultat == False:
      erreurs += 1

      if points != 0:
        points -= 1
    else:
      points += 1
    # Affiche les changements de points
    écran_retroaction.addstr(2, 0, f"Points: {points}")
    écran_retroaction.refresh()
    time.sleep(1.5)
  