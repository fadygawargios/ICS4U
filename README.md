# ICS4U

## Objectifs

Ce programme python propose deux  jeux éducatifs, Énigme Nationale et Pengouins du Tri respectivement selon l'âge des utilisateurs. Il fournit également des commentaires, des messages de bienvenu et de fin personnalisés ainsi qu'un systéme de score différente selon une difficulté choisi. 

## Jeux

### Jeu 1 : Énigme Nationale (3e à la 4e année d'étude)

**Description:** Dans Énigme Nationale, l'élève devra choisir le nom d'un pays parmi trois choix à partir d'une carte mondiale ou d'un drapeau. L'objectif est d'atteindre un certain score en accumulant des points corrects.

### Jeu 2 : Pingouins du Tri (1re à la 2e année d'étude)

**Description:** Dans Pingouins du Tri, l'élève aidera les pingouins à ranger leurs poissons en les classant par ordre croissant ou décroissant, selon les instructions données à l'écran. Un feedback personnalisé les guidera en cas d'erreur.

P.S: L'algorithme du tri utulisé s'agit de Merge Sort - Éfficacité: O(n log n).

## Dépendances

Pour exécuter le programme, vous avez besoin de:

1. Python 3: 
  Installer à: https://www.python.org/downloads/

2. Git Bash: 
  Installer à: https://git-scm.com/downloads

3. Les fichiers listés dans `requirements.txt`:

* windows-curses==2.3.2 (ou version équivalent selon le OS)
* deep_translator==1.11.4
* Pillow==10.2.0
* pycountry==23.12.11
* PyGetWindow==0.0.9

Pour tout installer exécuter : `pip install -r requirements.txt`

## Exécution

1. Ouvrez Git Bash et naviguez vers le répertoire contenant le programme.
2. Exécutez le programme en tapant `python main.py`