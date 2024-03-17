import pycountry
from deep_translator import GoogleTranslator
import curses
from curses.textpad import Textbox, rectangle
import pygetwindow as gw
from random import randint
import time

# Définit la constante des trois difficultés possibles
DIFFICULTÉS = ["Facile", "Moyenne", "Difficile"]

# Définit la constante du touche ENTER en ASCII
ENTER = 10


# todo: **LES FONCTIONS DOIVENT UTULISER LA MEME NOTATION (camelCase ou snake_case)

# Fonction qui crée des options, un sous-liste aléatoire d'une liste passée
def ObtenirOptions(list):

  # Définit la longeur de la liste - 1 pour la génération de nombres aléatoires
  longueur = len(list) - 1
  
  # Définit les listes pour contenir les options et les noms de ffichiers respectifs
  options = []
  options_nom_fichiers = []

  # Définit une liste pour contenir les nombres aléatoires pour éviter les doublons
  nombres_aleatoires = []

  # Creation de 3 options:
  for i in range(3):
    # Génére un nombre aléatoire entre 0 et la longeur de la liste
    nombres_aleatoire = randint(0, longueur)
    # Trouve le nom d'un fichier aléatoire (ce qui correspond à l'index de nombres_aléatoires) 
    fichier_aleatoire = list[nombres_aleatoire]
    # Transforme le nom du ficher en nom de pays
    counry_name = FichierVersNom(fichier_aleatoire)

    # Si le nombre_aléatoire était déja obtenu
    if nombres_aleatoire in nombres_aleatoires:
      # Cherche un nouveau
      nombres_aleatoire = randint(0, longueur)
    
    # Ajoute le nombre_aléatoire qu'on vient de voir dans la liste
    nombres_aleatoires.append(nombres_aleatoire)
    # Ajoute le nom du pays dans options et le noms du fichier correspondantes dans options_nom_fichiers
    options.append(counry_name)
    options_nom_fichiers.append(fichier_aleatoire)

  # Retourne les options, leurs nom de fichiers et une int aléatoire comme index de la bonne réponse du liste options
  return options, options_nom_fichiers, randint(0, len(options) - 1)

    
# Fonction qui ferme le fenetre d'image ouverte
def FermeImage():
  # Pour chaque fenetre "Photos" (celui qui l'ouvre l'image sur Windows)
  for fenetre in gw.getWindowsWithTitle(f"Photos"):
    # Ferme le
    fenetre.close()

# Fonction qui prend le nom d'un fichier et retourne le nom du pays
def FichierVersNom(file):
  # *Sachez que les fichiers sont nommés avec le code du pays et l'extension .jpg (ex: ca.jpg pour Canada)

  # Enleve l'extension
  code = file.split(".jpg", 1)[0]
  # Cherche l'info du pays en anglais avec le code
  info_pays_en = pycountry.countries.get(alpha_2=code)
  # Sort seulement le nom de tout l'information disponible
  nom_pays_en = str(dict(info_pays_en)["name"])
  # Traduit le nom du pays en francais pour l'utulisateur
  nom_pays_fr = GoogleTranslator(source='auto', target='fr').translate(nom_pays_en)
  # Enleve des info inutile du nom
  nom_pays_fr = nom_pays_fr.split(",", 1)[0]
  nom_pays_fr = nom_pays_fr.split("(", 1)[0]

  # Retourne le nom en francais
  return nom_pays_fr

# stdscr -> "standard screen"
# Fonction appelée par main() pour imprimer l'introduction et commencer le jeu
def Démarrage(stdscr):
  WHITE_AND_YELLOW = curses.color_pair(1)
  # Assure qu'il y aura un délai jusqu'à l'utulisateur appuie un bouton
  stdscr.nodelay(False)

  # Enleve le curseur de l'utulisateur
  curses.curs_set(0)

  # Enleve tout sur l'écran standard avant d'imprimer les messages d'introduction
  # Paramètres: stdscr.addstr(position_y, position_x, "str du message", attribue_1 | attribue_2)
  stdscr.clear()
  stdscr.addstr(1, 0, "Bienvenu aux jeux éducatives :)", WHITE_AND_YELLOW | curses.A_BOLD)
  # todo: work on prompts and explanations
  
  stdscr.addstr(2, 0, "Selon votre année scolaire, vous allez étre assigner un jeux...")
  stdscr.addstr(3, 0, "Cliquez sur n'importe quelle bouton pour commencer!")
  stdscr.refresh()
  stdscr.getch()
  stdscr.clear()

  # Demande l'utulisateur pour son nom
  écran_info = curses.newwin(6, 105, 0, 0)
  info_utulisateur = PoseText(écran_info, "Veuillez écrire votre prénom et votre année séparer par une espace:")
  nom = info_utulisateur[0]
  année = int(info_utulisateur[1])
  stdscr.addstr(0, 0, f"Salut {nom}")

  stdscr.addstr(2, 0, "SVP cliquer un bouton pour choisir une difficulté")
  stdscr.addstr(3, 0, "En mode facile vous aurez besoin de 5 points, en mode moyenne, 10 points et mode difficile, 15 points pour gagner!")
  stdscr.addstr(5, 0, "ATTENTION:", curses.A_STANDOUT)
  stdscr.addstr(5, 11, "Vous perdez des points si vous répondez mal! Bonne chance!")
  # Fait un refresh à l'écrain pour afficher les changements
  stdscr.refresh()

  # Attend pour n'importe quelle clique de boutton
  stdscr.getch()

  # Demande l'utulisateur à quelle difficulté il aimerait jouer
  question = "Choisir une difficulté:"
  difficulté = PoseMultiple(stdscr, DIFFICULTÉS, question)
  
  # Retourne l'index du difficulté choisi
  return DIFFICULTÉS.index(difficulté), int(année)

# Fonction appelée par main() pour imprimer la conclusion et finir le jeu
def ÉcranFin(stdscr, erreurs):
  
  WHITE_AND_YELLOW = curses.color_pair(1)
  WHITE_AND_GREEN = curses.color_pair(3)

  # Assure qu'il y aura un délai jusqu'à l'utulisateur appuie un bouton
  stdscr.nodelay(False)

  # Enleve les question en effacant l'écain
  stdscr.clear()

  # Imprime la conclusion à travers 3 lignes
  stdscr.addstr("BRAVO!! VOUS AVEZ GAGNER!!", WHITE_AND_GREEN)
  stdscr.addstr(1,0, f"Vous avez faite {erreurs} erreurs.")
  stdscr.addstr(2,0,  "Pour fermer le jeu, appuyer")
  stdscr.addstr(2, 28, "ENTER", curses.A_STANDOUT)
  stdscr.addstr(3, 0, "Merci d'avoir jouer Énigme Nationale :)", WHITE_AND_YELLOW)


  # Affiche la conclusion
  stdscr.refresh()

  # Attend l'utulisateur d'appuyer un boutton afin de retourner ce qui fini le jeu
  stdscr.getch()


# Fonction qui affiche les options et permette le selectionnement
def ListeQuestions(écran_questions, ligne_sélectionnée, options):
  WHITE_AND_YELLOW = curses.color_pair(1)

  # Pour chaque question dans option
  for indice_question in range(len(options)):
  # Si la question est séléctionné
    if ligne_sélectionnée == indice_question:
      # Écrit le en couleur sur une différent ligne (celui qui correspon à indice question)
      écran_questions.addstr(indice_question, 0, f"{indice_question + 1}.{options[indice_question]}", WHITE_AND_YELLOW)
  
    # Sinon imprime le sans couleur
    else:
      écran_questions.addstr(indice_question, 0, options[indice_question])
  
  # Affiche tout les changements 
  écran_questions.refresh()

# Fonction qui pose une question à l'utulisateur à partir d'options
def PoseMultiple(stdscr, options, question):
  
  # Permettent que le programme puisse continuer à jouer quand l'utulisateur ne clique pas des boutons
  stdscr.nodelay(True)
  # Enleve le curseur
  curses.curs_set(0)
  # Efface l'écran
  stdscr.clear()
  # Imprime la question
  stdscr.addstr(question, curses.A_BOLD)
  # Imprime des consignes sur comment naviguer sur le ligne d'en dessous
  stdscr.addstr(1, 0, "Utulisez les touches ARROW: ↑, ↓ pour naviguer et ENTER pour séléctionner.")
  # Affiche les changements
  stdscr.refresh()

  # Checher les dimensions y et x du line de commande
  dimensions = stdscr.getmaxyx()
  # Prend la deuxiéme valeur du Tuple -> la largeur
  largeur = dimensions[1]
  # Crée un nouveau écran au dessus de stdscr qui est de 3 colonnes et de largeur max -1
  # et qui débute 2 lines en dessous du 0
  écran_questions = curses.newwin(3, largeur - 1 , 2, 0)
    
  # Définit le colonne séléctionnée sur l'écran écran_questions
  ligne_sélectionnée = 0

  # Définit les touches que l'utulisateur clique
  touche = None

  # Tandis que l'utulisateur n'a pas cliqué ENTER
  while touche != ENTER:

    # Essaie de détécter de l'input
    try:
      touche = stdscr.getch()
    except:
      touche = None
    
    # Si le boutton UP est clicqué et qu'il y a de la place pour bougé UP
    if touche == curses.KEY_UP and ligne_sélectionnée >= 1:
      # Bouge le ligne selectionée vers le haut
      ligne_sélectionnée -= 1
    
    # Si le boutton DOWN est clicqué et qu'il y a de la place pour bougé DOWN
    elif touche == curses.KEY_DOWN and ligne_sélectionnée < len(options) - 1:
      # Bouge le ligne selectionée vers le bas
      ligne_sélectionnée += 1

    # Affiche les options selon la ligne_sélectionnée
    ListeQuestions(écran_questions, ligne_sélectionnée, options)

    # Efface les options entre modification (pour qu'ils ne superimposent pas)
    écran_questions.clear()
  
  # Retourne l'option sélectionné quand l'utulisateur à cliqué ENTER
  return options[ligne_sélectionnée]

# todo: fix having to click enter several times
# Fonction qui pose l'utulisateur pour so nom et année d'étude
def PoseText(écran, question):
  # Donne le curseur au utulisateur
  curses.curs_set(1)
  # Permettent que le programme puisse continuer à jouer quand l'utulisateur ne clique pas des boutons
  écran.nodelay(True)

  écran.clear()

  # Ajoute la question
  écran.addstr(0, 0, question)
  # Affiche la question
  écran.refresh()

  # Crée un endroit pour l'utulisateur à écrire
  écran_texte = curses.newwin(1, 50, 2, 0)
  endroit_texte = Textbox(écran_texte)

  # Tandis que l'utulisateur n'appuie pas ENTER, permet lui d'écrire
  touche = None
  while touche != ENTER:
    endroit_texte.edit()
    touche = écran_texte.getch()
    
 

  # Prend l'info du endroite_texte
  infos = endroit_texte.gather()
  
  # todo: add comments to explain what this does
  info_list = infos.split(" ")

  # Retourne les informations en forme de liste
  return info_list


# todo: add comments
def listeHasard(longeur, min, max): 
  liste = []
  for i in range(longeur):
    liste.append(randint(min, max))
  return liste

# todo: add comments
def mergeSort(list, croissant):
  if len(list) <= 1:
    return list

  middle = len(list) // 2
  leftList = list[:middle]
  rightList = list[middle:]
  leftList = mergeSort(leftList, croissant)
  rightList = mergeSort(rightList, croissant)
  return merge(leftList, rightList, croissant)
  

def merge(leftList, rightList, croissant):
  merged_list = []
  left_length = len(leftList)
  right_length = len(rightList)
  l = 0
  r = 0

  while l < left_length and r < right_length:
    if croissant == True:
      if leftList[l] < rightList[r]:
        merged_list.append(leftList[l])
        l += 1
      else:
        merged_list.append(rightList[r])
        r += 1
    else:
      if leftList[l] > rightList[r]:
        merged_list.append(leftList[l])
        l += 1
      else:
        merged_list.append(rightList[r])
        r += 1

  # the remaining number if the list arent the same size
  while l < left_length:
    merged_list.append(leftList[l])
    l += 1
  
  # the remaining number if the list arent the same size
  while r < right_length:
    merged_list.append(rightList[r])
    r += 1

  return merged_list

def formatList(liste):
  liste_formatted = ""
  for i in range(len(liste)):
    if i != len(liste) - 1:
      liste_formatted = liste_formatted + str(liste[i]) + ", "
    else:
      liste_formatted = liste_formatted + str(liste[i])

  return liste_formatted

# todo: translate comments into french
def print_ascii_art(screen):
  # Define starting position (y, x)
  y = 1  # Start from the second row (avoiding the top line)
  x = 5   # Adjust this for desired horizontal centering

  art_lines = [
      "",
      "                 .88888888:.",
      "                88888888.88888.",
      "              .8888888888888888.",
      "              888888888888888888",
      "              88' _`88'_  `88888",
      "              88 88 88 88  88888",
      "              88_88_::_88_:88888",
      "              88:::,::,:::::8888",
      "              88`:::::::::'`8888",
      "             .88  `::::'    8:88.",
      "            8888            `8:888.",
      "          .8888'             `888888.",
      "         .8888:..  .::.  ...:'8888888:.",
      "        .8888.'     :'     `'::`88:88888",
      "       .8888        '         `.888:8888.",
      "      888:8         .           888:88888",
      "    .888:88        .:           888:88888: ",
      "    8888888.       ::           88:888888",
      "    `.::.888.      ::          .88888888",
      "   .::::::.888.    ::         :::`8888'.:.",
      "  ::::::::::.888   '         .::::::::::::",
      "  ::::::::::::.8    '      .:8::::::::::::.",
      " .::::::::::::::.        .:888:::::::::::::",
      " :::::::::::::::88:.__..:88888:::::::::::'",
      "  `'.:::::::::::88888888888.88:::::::::'",
      "      `':::_:' -- '' -'-' `':_::::'`",
      " "
  ]

  # Print each line of art with increasing y-value
  for line in art_lines:
    screen.addstr(y, x, line)
    y += 1

def VérifieRéponse(réponse, bonne_réponse, écran_retroaction):
  WHITE_AND_RED = curses.color_pair(2)
  WHITE_AND_GREEN = curses.color_pair(3)
 # Si la réponse de l'utilisateur est la bonne réponse
  if str(réponse) == str(bonne_réponse):

    # Imprime la rétroaction sur le window «écran_retroaction»
    écran_retroaction.clear()
    écran_retroaction.addstr(f"Bonne Réponse! Bravo!", WHITE_AND_GREEN | curses.A_BOLD)
    écran_retroaction.refresh()
    
    return True

  else:

    # Imprime la rétroaction sur le window «écran_retroaction»
    écran_retroaction.clear()
    écran_retroaction.addstr(f"Mauvaise Réponse! La réponse était {bonne_réponse}.", WHITE_AND_RED | curses.A_BOLD)
    écran_retroaction.refresh()

    return False