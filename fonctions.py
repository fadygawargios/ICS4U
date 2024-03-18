import pycountry
from deep_translator import GoogleTranslator
import curses
from curses.textpad import Textbox
import pygetwindow as gw
from random import randint
import sys
import time

# Définit la constante des trois difficultés possibles
DIFFICULTÉS = ["Facile", "Moyenne", "Difficile"]

# Définit la constante du touche ENTER en ASCII
ENTER = 10

# Fonction qui crée des options, un sous-liste aléatoire d'une liste passée
def obtenir_options(list):

  # Définit la longeur de la liste - 1 pour la génération de nombres aléatoires
  longueur = len(list) - 1
  
  # Définit les listes pour contenir les options et les noms de ffichiers respectifs
  options = []
  options_nom_fichiers = []

  # Définit une liste pour contenir les nombres aléatoires pour éviter les doublons
  nombres_aleatoires = []

  # Creation de 3 options:
  options_à_chercher = 3
  while options_à_chercher != 0:

    # Génére un nombre aléatoire entre 0 et la longeur de la liste
    nombre_aleatoire = randint(0, longueur)
    
    # Si le nombre n'a pas était vu encore
    if nombre_aleatoire not in nombres_aleatoires:
      
      # Ajoute le nombre_aléatoire qu'on vient de voir dans la liste
      nombres_aleatoires.append(nombre_aleatoire)

      # Trouve le nom d'un fichier aléatoire (ce qui correspond à l'index de nombres_aléatoires) 
      fichier_aleatoire = list[nombre_aleatoire]

      # Transforme le nom du ficher en nom de pays
      nom_pays = fichier_vers_nom(fichier_aleatoire)

      # Ajoute le nom du pays dans options et le noms du fichier correspondantes dans options_nom_fichiers
      options.append(nom_pays)

      options_nom_fichiers.append(fichier_aleatoire)
      
      # Un moins d'options qui reste à chercher
      options_à_chercher -= 1

  # Retourne les options, leurs nom de fichiers et une int aléatoire comme index de la bonne réponse du liste options
  return options, options_nom_fichiers, randint(0, len(options) - 1)

    
# Fonction qui ferme le fenetre d'image ouverte
def ferme_image():
  # Pour chaque fenetre "Photos" (celui qui l'ouvre l'image sur Windows)
  for fenetre in gw.getWindowsWithTitle(f"Photos"):
    # Ferme le
    fenetre.close()

# Fonction qui prend le nom d'un fichier et retourne le nom du pays
def fichier_vers_nom(file):
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
def démarrage(stdscr):

  BLANC_ET_JAUNE = curses.color_pair(1)
  # Assure qu'il y aura un délai jusqu'à l'utulisateur appuie un bouton
  stdscr.nodelay(False)

  # Enleve le curseur de l'utulisateur
  curses.curs_set(0)

  # Enleve tout sur l'écran standard avant d'imprimer les messages d'introduction
  # Paramètres: stdscr.addstr(position_y, position_x, "str du message", attribue_1 | attribue_2)
  stdscr.clear()
  stdscr.addstr(1, 0, "Bienvenu aux jeux éducatives :)", BLANC_ET_JAUNE | curses.A_BOLD)

  # Explique les jeux possible selon l'age de l'utulisateur
  stdscr.addstr(2, 0, "Selon votre année scolaire, vous allez être assigner un jeux:")
  stdscr.addstr(3, 0, "1e-2e année : ", curses.A_BOLD)
  stdscr.addstr(3, 15, "PINGOUINS DU TRI", BLANC_ET_JAUNE | curses.A_BOLD)
  stdscr.addstr(4, 0, "3e-4e année : ", curses.A_BOLD)
  stdscr.addstr(4, 15, "ÉNIGME NATIONALE", BLANC_ET_JAUNE | curses.A_BOLD)

  # Explique comment démarer le programme
  stdscr.addstr(5, 0, "Cliquez sur n'importe quelle bouton pour commencer!")
  
  # Fait un refresh à l'écran pour afficher les changements
  stdscr.refresh()
  
  # Attend pour n'importe quelle clique de boutton
  stdscr.getch()
  
  # Efface l'écran
  stdscr.clear()

  # Demande l'utulisateur pour son nom dans un nouveau écran
  écran_info = curses.newwin(6, 105, 0, 0)
  info_utulisateur = pose_texte(écran_info, "Veuillez écrire votre prénom: ")
  
  # pose_texte retourne une liste d'information, le premier élément s'agit du nom fourni dans ce cas
  nom = info_utulisateur[0]

  # Établit la question et les groupes ages possibles
  question = "En quelle année d'études êtes-vous?"
  groupe_ages = ["| 1ère - 2ème année", "| 3e - 4e année", "| +5e année"]

  année = pose_multiple(stdscr, groupe_ages, question)
  
  # Assure qu'il y aura un délai jusqu'à l'utulisateur appuie un bouton
  stdscr.nodelay(False)

  # Si l'utulisateur est trop vieux pour jouer
  if "+5" in année: 
    stdscr.clear()

    # Explique le
    stdscr.addstr(0, 0, "Malheureusement, vous êtes trop vieux pour jouer aux jeux disponibles.", curses.A_BOLD)
    stdscr.addstr(1, 0, "Cliquez sur n'importe quelle bouton pour terminer.")
    stdscr.refresh()

    # Attend pour un touche comme confirmation
    stdscr.getch()

    # Sort du programme avec code 0: aucun erreur
    sys.exit(0)

  # Efface la question pour imprimer l'accueille
  stdscr.clear()

  # Accueille l'utilisateur par nom et explique les difficultés
  stdscr.addstr(0, 0, f"Salut {nom}")
  stdscr.addstr(2, 0, "SVP cliquer un bouton pour choisir une difficulté.")
  stdscr.addstr(3, 0, "En mode facile vous aurez besoin de 5 points, en mode moyenne, 10 points et mode difficile, 15 points pour gagner!")
  stdscr.addstr(5, 0, "ATTENTION:", curses.A_STANDOUT)
  stdscr.addstr(5, 11, "Vous perdez des points si vous répondez mal! Bonne chance!")
  
  # Fait un refresh à l'écran pour afficher les changements
  stdscr.refresh()
  
  # Attend pour un touche avant de procéder
  stdscr.nodelay(False)
  stdscr.getch()

  stdscr.clear()

  # Demande l'utulisateur à quelle difficulté il aimerait jouer
  question = "Choisir une difficulté:"
  difficulté = pose_multiple(stdscr, DIFFICULTÉS, question)

  # Retourne l'index du difficulté choisi, le nom et l'année de l'utulisateur en liste
  return DIFFICULTÉS.index(difficulté), nom, année


# Fonction appelée par main() pour imprimer la conclusion et finir le jeu
def écran_fin(stdscr, erreurs, nom):
  
  BLANC_ET_JAUNE = curses.color_pair(1)
  BLANC_ET_VERT = curses.color_pair(3)

  # Assure qu'il y aura un délai jusqu'à l'utulisateur appuie un bouton
  stdscr.nodelay(False)

  # Enleve les question en effacant l'écain
  stdscr.clear()

  # Imprime la conclusion à travers 3 lignes
  nom = nom.upper()
  stdscr.addstr(f"BRAVO {nom}!! VOUS AVEZ GAGNER!!", BLANC_ET_VERT)
  stdscr.addstr(1,0, f"Vous avez faite {erreurs} erreurs.")
  stdscr.addstr(2,0,  "Pour fermer le jeu, appuyer")
  stdscr.addstr(2, 28, "ENTER", curses.A_STANDOUT)
  stdscr.addstr(3, 0, "Merci d'avoir jouer :)", BLANC_ET_JAUNE)

  # Affiche la conclusion
  stdscr.refresh()

  # Attend l'utulisateur d'appuyer un boutton afin de retourner ce qui fini le jeu
  stdscr.getch()


# Fonction qui affiche les options et permette le selectionnement
def liste_questions(écran_questions, ligne_sélectionnée, options):
  BLANC_ET_JAUNE = curses.color_pair(1)

  # Pour chaque question dans option
  for indice_question in range(len(options)):
  # Si la question est séléctionné
    if ligne_sélectionnée == indice_question:
      # Écrit le en couleur sur une différent ligne (celui qui correspon à indice question)
      écran_questions.addstr(indice_question, 0, f"{indice_question + 1}.{options[indice_question]}", BLANC_ET_JAUNE)
  
    # Sinon imprime le sans couleur
    else:
      écran_questions.addstr(indice_question, 0, options[indice_question])
  
  # Affiche tout les changements 
  écran_questions.refresh()

# Fonction qui pose une question à l'utulisateur à partir d'options
def pose_multiple(stdscr, options, question):
  
  # Permettent que le programme puisse continuer à jouer quand l'utulisateur ne clique pas des boutons
  stdscr.nodelay(True)
  # Enleve le curseur
  curses.curs_set(0)
  # Efface l'écran
  stdscr.clear()
  # Imprime la question
  stdscr.addstr(question, curses.A_BOLD)
  # Imprime des consignes sur comment naviguer sur le ligne d'en dessous
  stdscr.addstr(1, 0, "Utulisez les touches ")
  stdscr.addstr(1, 21, "ARROW: ↑, ↓", curses.A_STANDOUT)
  stdscr.addstr(1, 33, "pour naviguer et ")
  stdscr.addstr(1, 50, "ENTER", curses.A_STANDOUT)
  stdscr.addstr(1, 56, "pour séléctionner.")
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
    liste_questions(écran_questions, ligne_sélectionnée, options)

    # Efface les options entre modification (pour qu'ils ne superimposent pas)
    écran_questions.clear()
  
  # Retourne l'option sélectionné quand l'utulisateur à cliqué ENTER
  return options[ligne_sélectionnée]

# Fonction qui pose l'utulisateur pour so nom et année d'étude
def pose_texte(écran, question):

  # Donne le curseur au utulisateur
  curses.curs_set(1)
  # Permettent que le programme puisse continuer à jouer quand l'utulisateur ne clique pas des boutons
  écran.nodelay(True)

  écran.clear()

  # Ajoute la question
  écran.addstr(0, 0, question, curses.A_BOLD)
  écran.addstr(1, 0, "Écrivez dans la case ci-dessous, puis cliquez sur      .")
  écran.addstr(1, 50, "ENTER", curses.A_STANDOUT)
  # Affiche la question
  écran.refresh()

  # Crée un endroit pour l'utulisateur à écrire
  écran_texte = curses.newwin(1, 50, 3, 0)
  endroit_texte = Textbox(écran_texte)

  # Tandis que l'utulisateur n'appuie pas ENTER, permet lui d'écrire
  touche = None
  while touche != ENTER:
    endroit_texte.edit()
    touche = écran_texte.getch()
    
  # Prend l'info du endroite_texte
  infos = endroit_texte.gather()

  # Sépare le réponse de l'utulisateur en une liste de valeur à partir des espaces blanches 
  info_list = infos.split(" ")

  # Retourne la liste d'informations
  return info_list


# Crée une liste avec une certaine longeur, contenant des nombres au hasard entre min et max
def liste_hasard(longeur, min, max): 
  liste = []

  # Lorsque la longeur désirée n'est pas atteint
  while longeur != 0:
    # Cherche un nombre aléatoire
    nombre_aléatoire = randint(min, max)
    # Si le nombre n'a pas était déja utulisé pour cette question
    if nombre_aléatoire not in liste:
      # Ajoute le au liste
      liste.append(nombre_aléatoire)
      # Soustrais du longeur parce qu'on vient de chercher un nombre
      longeur -= 1
      
  return liste

# Algorithmes de tri du type «Divide & Conquer»
def merge_sort(liste, croissant):
  
  # Cas de base (s'il n'y est plus possibile de subdiviser)
  if len(liste) <= 1:
    return liste

  # Trouve l'élément à peu prés au milieu de la liste (pas exactement s'il y a un nombre impair)
  middle = len(liste) // 2
  # Subdivise la liste originale en deux 
  liste_gauche = liste[:middle]
  liste_droite = liste[middle:]
  # Subdivision récursive
  liste_gauche = merge_sort(liste_gauche, croissant)
  liste_droite = merge_sort(liste_droite, croissant)
  # Fusion de tout les parties de la liste (chaqun un est déja triée)
  return merge(liste_gauche, liste_droite, croissant)
  
# Fusionnent deux listes (la fonction qui fait les compairasons: < et >)
def merge(liste_gauche, liste_droite, croissant):

  # Définie les variables intiales
  liste_fusionnée = []
  longeur_gauche = len(liste_gauche)
  longeur_droite = len(liste_droite)
  l = 0
  r = 0

  # Tandis qu'il ya des éléments dans n'importe quel liste
  while l < longeur_gauche and r < longeur_droite:
    # Si la fonction doit trier par ordre croissant
    if croissant == True:
      # Si l'élément du liste gauche est plus petit 
      if liste_gauche[l] < liste_droite[r]:
        # Ajoute le au liste triée
        liste_fusionnée.append(liste_gauche[l])
        # Bouge de un dans la liste gauche (puisque on vient de bien triée la valeur)
        l += 1
       # Si l'élément du liste droite est plus petit ou s'ils sont du meme taille
      else:
        # Ajoute celui du liste droite
        liste_fusionnée.append(liste_droite[r])
        # Bouge de un dans la liste droite (puisque on vient de bien triée la valeur)
        r += 1
    # Si la fonction doit trier par ordre décroissant
    else:
      # Signe inverse, on ajoute l'élément le plus grand en premier
      if liste_gauche[l] > liste_droite[r]:
        liste_fusionnée.append(liste_gauche[l])
        l += 1
      else:
        liste_fusionnée.append(liste_droite[r])
        r += 1

  # S'il reste des éléments dans la liste gauche
  # puisque les listes ne sont pas toujours du meme taille s'il y a un nombre impaire d'éléments 
  while l < longeur_gauche:
    # Ajoute les
    liste_fusionnée.append(liste_gauche[l])
    l += 1
  
  # S'il reste des éléments dans la liste droite
  while r < longeur_droite:
    liste_fusionnée.append(liste_droite[r])
    r += 1

  # Retourne la liste fusionner et bien triée
  return liste_fusionnée

# Fonction qui rend les valeurs d'une liste plus user-friendly en le formattant en string 
def format_liste(liste):
  # String du liste à imprimer
  liste_formattée = ""

  # Ajoute les valeurs avec des virgules entre
  for i in range(len(liste)):
    if i != len(liste) - 1:
      liste_formattée = liste_formattée + str(liste[i]) + ", "
    else:
      liste_formattée = liste_formattée + str(liste[i])

  return liste_formattée

# Fonction qui imprime de l'art ASCII pour les jeux
def imprime_art(screen, jeu):
  # Définie les cordonnée intiales de l'art
  y = 1  
  x = 5   

  # Définie la piéce d'art selon le jeu
  # sources: https://ascii.co.uk/art
  # JEU 1: Énigme Nationale
  if jeu == 1:
    liste_art = [
      ".. . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
      ".. . . . . . . .#######. . . . . . . . . . . . . . . . .",
      ".. . . . . . .#. .#### . . . ####. . .###############. . .",
      ".. . ########. ##. ##. . . ######################### . . .",
      ".. . . ##########. . . . ######################. . . . . .",
      ".. . . .######## . . . .   ################### . . . . . .",
      ".. . . . ### .   . . . .#####. ##############. # . . . . .",
      ".. . . . . ##### . . . .#######. ##########. . . . . . . .",
      ".. . . . . .###### . . . .#### . . . . .## . . . . . . . .",
      ".. . . . . . ##### . . . .#### # . . . . . ##### . . . . .",
      ".. . . . . . ### . . . . . ##. . . . . . . . ### .#. . . .",
      ".. . . . . . ##. . . . . . . . . . . . . . . . . . . . . .",
      ".. . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
  ]
  # JEU 2: Pingouins du Tri
  else:
    liste_art = [
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

  # Imprime chaque ligne du liste sur une différent ligne dans la ligne de commande
  for ligne in liste_art:
    screen.addstr(y, x, ligne)
    y += 1

# Fonction qui vérifie si l'utulisateur à bien réondu et fourni de la rétroaction sinon
def vérifie_réponse(réponse, bonne_réponse, écran_retroaction):
  BLANC_ET_ROUGE = curses.color_pair(2)
  BLANC_ET_VERT = curses.color_pair(3)

 # Si la réponse de l'utilisateur est la bonne réponse
  if str(réponse) == str(bonne_réponse):

    # Imprime la rétroaction sur le window «écran_retroaction»
    écran_retroaction.clear()
    écran_retroaction.addstr(f"Bonne Réponse! Bravo!", BLANC_ET_VERT | curses.A_BOLD)
    écran_retroaction.refresh()
    
    # Retourne Vrai pour augmenter le nombre de points
    return True

  # Sinon
  else:
    
    écran_retroaction.clear()
    
    # Si la bonne réponse est du type liste (partie du jeu de tri)
    if type(bonne_réponse) == list:
      # Donne l'utulisateur 5 secondes pour vérifier leur rétroaction
      temps_rétroaction = 5
      
      # Imprime la bonne réponse sans les paranthéses des listes
      bonne_réponse_str = str(bonne_réponse).strip("[]")
      écran_retroaction.addstr(0, 0, f"Mauvaise Réponse! La réponse était {bonne_réponse_str}.", BLANC_ET_ROUGE | curses.A_BOLD)

      # Donne de la rétroaction
      écran_retroaction.addstr(1, 0, "Voici les erreurs dans votre réponse:")
    
      # Si l'utulisateur a mis trop de nombres
      if len(réponse) > 5:
        écran_retroaction.addstr(1, 38, "Vous avez mis trop d'éléments.")
      # Si l'utulisateur n'a pas mis assez de nombres
      elif len(réponse) < 5:
        écran_retroaction.addstr(1, 38, "Vous n'avez pas fourni assez d'éléments.")
      # Si l'utulisateur a bien mis 5 nombres
      else:
        # Vérifie chacun
        for num_index in range(5):
          # S'il n'est pas correcte, souligne le en rouge
          if réponse[num_index] != bonne_réponse[num_index]:
              écran_retroaction.addstr(1, 38 + (num_index * 3), f"{réponse[num_index]}", BLANC_ET_ROUGE)
          # Sinon, imprime le normalement
          else:
            écran_retroaction.addstr(1, 38 + (num_index * 3), f"{réponse[num_index]}")

    # Si la réponse n'est pas du type liste (partie du jeu ÉnigmeNationale)  
    else:
      # Réduit le temps de rétroaction
      temps_rétroaction = 0.5
      # Imprime tout simplement la bonne réponse
      écran_retroaction.addstr(f"Mauvaise Réponse! La réponse était {bonne_réponse}.", BLANC_ET_ROUGE | curses.A_BOLD)
    
    # Donne l'utulisateur le temps de vérifier la rétroaction
    écran_retroaction.refresh()
    time.sleep(temps_rétroaction)

    # Retourne faux puisqu'il a mal répondu à la question
    return False

# Fonction qui débute un jeu
def intro_jeu(stdscr, jeu):

  # Assigne les possibilités des jeux à des constantes
  ÉNIGME_NATIONALE = 1
  PINGOUINS_DU_TRI = 2

  # id d'un couleur à utuliser plus tard
  BLANC_ET_JAUNE = curses.color_pair(1)

  # Établit les informations nécessaires selon le jeu:

  if jeu == ÉNIGME_NATIONALE:
    # Espace s'agit de l'espace à laisser avant les message pour l'art ASCII
    espace = 65
    # nom du jeu
    nom = "ÉNIGME NATIONALE!!"
    # courte description de l'objectif du jeu séparer en deux lignes 
    description_ligne_1 = "Dans ce jeu, vous allez devoir identifier le nom"
    description_ligne_2 = "d'un pays à partir d'un drapeau ou d'une carte mondiale."
  
  if jeu == PINGOUINS_DU_TRI:
    espace = 50
    nom = "PINGOUINS DU TRI!!"
    description_ligne_1 = "Dans ce jeu, vous allez devoir mettre des suites de"
    description_ligne_2 = "nombres en ordre croissant et décroissant."

  # Assure qu'il y aura un délai jusqu'à l'utulisateur appuie un bouton
  stdscr.nodelay(False)
  
  # Imprime un message de bienvenu, une courte description et des consignes pour commencer
  stdscr.clear()
  stdscr.addstr(5, espace, "BIENVENU À", curses.A_BOLD)
  stdscr.addstr(5, espace + 11, f"{nom}", BLANC_ET_JAUNE | curses.A_BOLD)
  stdscr.addstr(6, espace, f"{description_ligne_1}")
  stdscr.addstr(7, espace, f"{description_ligne_2}")
  stdscr.addstr(8, espace, "Cliquez sur n'importe quelle bouton pour commencer!")
  
  # Imrpime l'art ASCII coresspondant au jeu
  if jeu == ÉNIGME_NATIONALE:
    imprime_art(stdscr, jeu=ÉNIGME_NATIONALE)
  else:
    imprime_art(stdscr, jeu=PINGOUINS_DU_TRI)

  stdscr.refresh()

  # Attend l'entrée de l'utilisateur avant de passer au jeu
  stdscr.getch()