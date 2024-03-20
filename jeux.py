import time
from PIL import Image
from common import *
from fonctions import (
    ferme_image,
    format_liste,
    intro_jeu,
    liste_hasard,
    obtenir_options,
    merge_sort,
    pose_multiple,
    pose_texte,
    vérifie_réponse,
)

# Pour plus d'info sur les jeux, visité le README.md

def énigme_nationale(stdscr, objectif, écran_retroaction):

  # Salue l'utulisateur au jeu 1: Énigme Nationale et imprime l'art ASCII correspondant
  intro_jeu(stdscr, jeu=1)
  
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

    # Compare le choix de l'utulisateur avec la bonne réponse et retourne un bool (vrai ou faux) correspondant
    résultat = vérifie_réponse(réponse, options[index_bonne_réponse], écran_retroaction)
    
    # Si l'tuulisateur a mal répondu
    if résultat == False:
      # Il a faite une erreur de plus
      erreurs += 1
      # Et si ses points ne sont pas déja 0
      if points != 0:
        # Soustrais un de son score
        points -= 1
    # Si l'utulisateur a bien répondu
    else:
      # Donne lui un point
      points += 1

    # Affiche les changements de points
    écran_retroaction.addstr(1, 0, f"Points: {points}")
    écran_retroaction.refresh()

    # Donne du temps à l'utulisateur de voir les changements de points avant la question prochaine
    time.sleep(1.5)

  # Retourne le nombre d'erreurs commit pour imprimer à l'écran
  return erreurs

def pingouins_du_tri(stdscr, objectif, écran_retroaction):
  
  # Salue l'utulisateur au jeu 2: Pingouins du tri et imprime l'art ASCII correspondant
  intro_jeu(stdscr, jeu=2)
  
  # Définit les points à 0
  points = 0

  # Montant d'erreurs que l'utulisateur a fait
  erreurs = 0

  # Lorsque l'utulisateur n'a pas atteint l'objectif de point
  while points != objectif:
    # Cherche une liste avec 5 ints aléatoires entre 1 et 100 (ce qui est non_triée)
    liste_non_triée = liste_hasard(longeur=5, min=1, max=100)

    # Efface l'écran (pour imprimer la question plus tard)
    stdscr.clear()
    
    # Si le pointage est paire
    if points % 2 == 0:
      # Forme une question de tri par ordre croissant
      question = f"QUESTION #{points + 1}: Met la suite de nombre suivante en ordre CROISSANT: " + format_liste(liste_non_triée)
      
      # Tri la liste_non_triée avec merge_sort en ordre croissant
      list_triée = merge_sort(liste_non_triée, croissant=True)

    # Si le pointage est impaire
    else:
      # Forme une question de tri par odre décroissant
      question = f"QUESTION #{points + 1}: Met la suite de nombre suivante en ordre DÉCROISSANT: " + format_liste(liste_non_triée)

      # Tri la liste en ordre décroissant (puisque croissant=False)
      list_triée = merge_sort(liste_non_triée, croissant=False)

    # Pose la question à l'utulisateur
    réponse = pose_texte(stdscr, question)
    
    # Place les numéros des réponses des utilisateurs dans une liste sans espaces ni virgules
    réponse_formatted = []
  
    for nombre in réponse:
      if nombre != "":
        réponse_formatted.append(int(nombre.replace(",", "")))

    # Vérifie si la question à était bien réussi, sinon, donne de la rétroaction sur «écran_rétroaction»
    résultat = vérifie_réponse(réponse_formatted, list_triée, écran_retroaction)
    
    # Sinon
    if résultat == False:
      # L'utulisateur a faite une erreur
      erreurs += 1

      # Si ses points ne sont pas déja 0
      if points != 0:
        # Enlève un
        points -= 1

    # Si la question a était bien réussi
    else:
      # Ajoute un point
      points += 1

    # Affiche les changements de points
    écran_retroaction.addstr(2, 0, f"Points: {points}")
    écran_retroaction.refresh()

    # Donne du temps à l'utulisateur de voir les changements de points avant la question prochaine
    time.sleep(1.5)

  # Retourne le nombre d'erreurs commit pour imprimer à l'écran
  return erreurs
  