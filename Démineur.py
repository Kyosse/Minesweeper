# -*- coding: utf-8 -*- Python 3.7.3
from random import *
import random
from tkinter import *
from operator import itemgetter
from datetime import datetime

# Initialisation de la variable pour contenir TOUS les noms avec leurs scores
score_plus_noms = []

# Création interface
main_windows = Tk()  # Attribut de la fenêtre pour séléctionner le mode de jeu
liste_scores = Listbox(main_windows, height=40, width=50)  # Affiche sur l'interface des scores avec le scroll


def _eleves():
    """
    Séparation des élèves des autres informations du fichier charactères
    le tout mise en fonction pour pouvoir être réinitialisé à chaque nouvelle partie global
    """
    with open('Characters.csv', mode='r', encoding='utf-8') as f:
        info = f.readlines()  # ouverture du fichier caractère et assimiliation a une liste
    eleves = []  # Créations du tableau des noms

    for i in range(len(info)):  # Boucle pour séparer chaque noms de info

        temporaire_eleve = info[i]  # Attribution de la ligne [a]
        temporaire_eleve = temporaire_eleve.split(';')  # Séparation des éléments avec ;
        eleves.append(temporaire_eleve[1])  # Ajout de la deuxieme colonne de la ligne dans la liste eleves
    eleves.remove("Name")  # On enlève "Name" qui ne fait pas parti des élèves
    return eleves


def partie(taille_tab):
    """
    Taille_tab définit la taille du Tableau
    Fonction qui calcul une partie de démineur de la taille du tableau définit
    Puis calcul et renvoie le score de la partie
    """

    # Création des variables:

    score_partie = 0  # Initialisation du score de la partie en cours

    # Seconde variable qui peut être agrandie pour servir de compteur dans while
    nbr_tours = taille_tab

    # Pour stocker les nombres aléatoires
    randligne = 0
    randcolonne = 0

    # Variable du nombre de cases restantes à dévoiler (Compte_cases est une variable intermédiaire)
    cases_libres = taille_tab ** 2
    compte_cases = 0

    # Variables de cases pour l'affichage du démineur dans console
    mine = "x"
    case_secrete = "o"  # Les cases qui ne sont pas encore dévoilées
    nombre_de_la_case = 0  # Pour compter le nombre de mine à côté d'une case

    # Création du tableau
    tab = [[case_secrete for _ in range(taille_tab)] for _ in range(taille_tab)]

    # Pour arrêter la partie en cas de défaite
    partie_perdue = False

    # Posage des mines aléatoirements
    while nbr_tours != 0:  # Boucle qui pose des bombes tant que le nb de bombes en fonction de taille_tab
        randligne = random.randint(0, (taille_tab - 1))
        randcolonne = random.randint(0, (taille_tab - 1))
        if tab[randligne][randcolonne] != mine:
            tab[randligne][randcolonne] = mine
            nbr_tours -= 1
    print(tab)  # Affichage dans la console la partie au tout début

    # Partie qui se joue
    nbr_tours = cases_libres
    while cases_libres > 0 and partie_perdue == False:  # Sortie de boucle avec utilisation des booléens
        randligne = random.randint(0, (taille_tab - 1))
        randcolonne = random.randint(0, (taille_tab - 1))
        if tab[randligne][randcolonne] == mine:  # Si mine touchée arrêter partie
            tab[randligne][randcolonne] = "Aïe"
            partie_perdue = True
        else:  # Sinon calculer le nombre de bombes autours
            if (randligne > 0 and randcolonne > 0) and tab[randligne - 1][randcolonne - 1] == mine:
                nombre_de_la_case += 1
            if randligne > 0 and tab[randligne - 1][randcolonne] == mine:
                nombre_de_la_case += 1
            if (randligne > 0 and randcolonne < taille_tab - 1) and tab[randligne - 1][randcolonne + 1] == mine:
                nombre_de_la_case += 1
            if randcolonne > 0 and tab[randligne][randcolonne - 1] == mine:
                nombre_de_la_case += 1
            if randcolonne < taille_tab - 1 and tab[randligne][randcolonne + 1] == mine:
                nombre_de_la_case += 1
            if (randligne < taille_tab - 1 and randcolonne > 0) and tab[randligne + 1][randcolonne - 1] == mine:
                nombre_de_la_case += 1
            if randligne < taille_tab - 1 and tab[randligne + 1][randcolonne] == mine:
                nombre_de_la_case += 1
            if (randligne < taille_tab - 1 and randcolonne < taille_tab - 1) and tab[randligne + 1][randcolonne + 1] \
                    == mine:
                nombre_de_la_case += 1
            tab[randligne][randcolonne] = nombre_de_la_case
            nombre_de_la_case = 0
            score_partie += 1
        for compte in range(taille_tab):
            compte_cases += tab[compte].count(case_secrete)
        cases_libres = compte_cases
    print(tab)  # Affichage dans la console la partie à la fin (avec toutes les tentatives)

    # verification des cases dévoilées pour le score
    if cases_libres == 0:
        score_partie = 50
        print(score_partie)
    else:
        print(score_partie)
    return score_partie


def score_final(j_temp, s_temp):
    """
    Calcule le score d'un joueur après toutes ses parties
    Et assimilation à la variable global score_plus_noms pour pouvoirs les stocker
    """

    score_fin_partie = [(j_temp, s_temp)]  # mise en liste du noms du joeur et de son score de la partie

    global score_plus_noms  # utilisation de la variable score qui est hors de la fonction
    score_plus_noms += score_fin_partie

    # fonction qui permet de trier dans l'odre sorted() avec itemgetter pour trier dans l'ordre décroissant
    score_plus_noms = sorted(score_plus_noms, key=itemgetter(1), reverse=True)
    return score_plus_noms


def eleve_joue(eleve):
    """
    Joue 10 parties aléatoirements et renvoie le score des 10 parties avec comme paramètre l'élève choisis au hasard
    """
    score = 0
    for _ in range(10):
        print("partie de", eleve)
        score += partie(4)
    return score


def partie_interface():
    """
    Lance 10 parties pour tous les élèves
    Puis calcul la moyenne de tous les scores
    """
    global score_plus_noms

    score_plus_noms = []  # Resmise à zéro de la variable pour pas avoir l'accumulation des scores lors du 2 tirage

    # Assimilations du temps actuel (heure,jour...) à la variable temps
    # puis utiliser cette date aléatoire dans seed pour avoir à chaque partit un "véritable" aléatoire
    temps = datetime.now()
    random.seed(temps)

    # Score totale pour calculer la moyenne
    score_total = 0

    eleves = _eleves()  # Attribution du résultat de la fonction à eleves

    # Lancement de toute les parties dans la longueur eleves
    for _ in range(len(eleves)):
        randeleves = random.randint(0, len(eleves) - 1)  # Piocher un élève aléatoire
        score_test = eleve_joue(eleves[randeleves])  # Elève joue 10 partie et assimile son score
        score_final(eleves[randeleves], score_test)  # Effectue la fonction avec comme paramètre l'élève et son score
        eleves.pop(randeleves)  # On enlève l'élève pour pas le repiocher
        score_total += score_test  # On ajoute le score de l'élève au score total pour  calculer la moyenne

    score_total = score_total / len(score_plus_noms)  # Calcule de la moyennne

    for i in range(len(score_plus_noms)):  # Affiche dans la console le noms et le score proprement
        print(f"{score_plus_noms[i][0]} - {score_plus_noms[i][1]}")
    print("moyenne totale des scores : ", score_total)

    for k in range(len(score_plus_noms)):  # Si une partie à déjà été jouée on supprime les scores de la liste
        liste_scores.delete(0)

    for i in range(len(score_plus_noms)):  # Ici on ajoute les scores dans la liste afficher dans l'interface
        liste_scores.insert(0 + i, score_plus_noms[i])
    liste_scores.grid()


def lancer():
    """
    La fonction lancer est le coeur du programme car c'est ici que l'interface pour lancer une partie est créée
    """

    # création des différents boutons

    bienvenue = Label(text="Bienvenue au démineur de Poudlard !!!!")
    bienvenue.grid()
    # Bouton pour lancer une partie
    lancer_partie = Button(main_windows, text='Lancer une partie', command=partie_interface)
    lancer_partie.grid()
    # Bouton pour lancer partie solo
    game_solo = Button(main_windows, text='Jouer tout seul(e)', command=lancer_partie_solo)
    game_solo.grid()
    quitter = Button(main_windows, text='Quitter', command=main_windows.destroy)  # Bouton pour fermer la fenêtre
    quitter.grid()
    main_windows.mainloop()


class JeuSolo():
    """
    class qui définit toutes les différentes actions pour la partie solo du démineur
    """

    def __init__(self):
        self.haut = 15
        self.long = 38  # Taille chageable du démineur
        self.mines = 65
        self.fenetre_demineur = Tk() # Création de l'interface
        self.fenetre_demineur.grid()
        self.grille = []  # Création de la liste qui va cette fois contenire des boutons avec lesquels on peut interagire
        for y in range(self.haut):
            self.grille.append([])
            for x in range(self.long):
                self.grille[y].append(" ") # Création des boutons et utilisations de bond pour assimiler une action précise aux boutons
                self.grille[y][x] = Button(height=0, width=3, font="Comic", text="", bg="gray78",
                                           command=lambda y=y, x=x: JeuSolo.click_gauche(self, y, x))
                self.grille[y][x].bind("<Button-3>", lambda cd_presser="<Button-3>",
                                                            y=y, x=x: JeuSolo.clic_droit(self, cd_presser, y, x))

                self.grille[y][x].grid(row=y, column=x) # Mise en place de la taille de la grille de bouton
                self.grille[y][x].mine = "False" # on définit les cases sans bombes en false pour les différenciés

        self.score_solo_final = 569
        self.score_solo = 0

        tableau = list(range(self.score_solo_final))

        emplacement_mines = []
        for _ in range(self.mines): # On fait une liste pour mettre des bombes aléatoires
            mine_temp = randint(0, len(tableau) - 1)
            emplacement_mines.append(tableau[mine_temp])
            del tableau[mine_temp]

        for i in range(len(emplacement_mines)): # Puis on assigne les positions des bombes dans la liste à notre grille de boutons
            x_valeur = int(emplacement_mines[i] % self.long) # Faites juste avant
            y_valeur = int(emplacement_mines[i] / self.long)

            self.grille[y_valeur][x_valeur].mine = "True" # On les définit à une valeur pour les reconaitres

        self.fenetre_demineur.mainloop()

    def click_gauche(self, y, x):
        affichage = ["gray20", "Blue", "Green", "Red", "Purple", "Black", "Maroon", "Gray", "Turquoise"]
        # Liste des différentes couleur pour les chiffres des nb de bombe
        if self.grille[y][x]["text"] != "F" and self.grille[y][x]["relief"] != "sunken": # Si la case n'est pas "enfoncée"
            if self.grille[y][x].mine == "False":
                self.score_solo += 1

                y_coo = [1, -1, 0, 0, 1, 1, -1, -1]  # Coordonnées des différentes cases autour de la case modifier
                x_coo = [0, 0, 1, -1, 1, -1, 1, -1]  # Exemple par rapport au centre (0,0) on regard la case (0,1) soit la case juste à droite
                # Dans l'ordre en haut, en bas, à gauche, à froite, en haut à gauche, en haut à droite,en bas à gauche, ne bas à droite
                nb_mines = 0
                for i in range(len(y_coo)):
                    tempi = y + y_coo[i] # Prise des coordonnées x et y pour ensuite pouvoir calculer les coordonnées alentours
                    tempx = x + x_coo[i]

                    # Methodes pour compter les bombes de manières plus optimisée tiré d'une vidéo
                    if tempi < self.haut and tempx < self.long and tempi >= 0 and tempx >= 0:  # On regard les coos tout autour
                        if self.grille[tempi][tempx].mine == "True":  # Et on ajoute 1 pour chaque bombe des 8 cases aux alentours
                            nb_mines += 1

                if nb_mines == 0:  # Si pas de bombe alors la case reste vide
                    nb_mines = ""

                self.grille[y][x].configure(text=nb_mines, relief="sunken", bg="gray85")  # Ici on modifie le bouton
                # pour le nommer x nombres de bombes et le laisser dans l'affichage enfoncer(sunken)
                if str(nb_mines).isdigit():
                    self.grille[y][x].configure(fg=affichage[nb_mines])  # On finit par mettre la couleur en fonction du nombre

                if nb_mines == "": # Si les cases non pas de chiffre alors on calcul toutes les cases vides autours
                    for z in range(len(y_coo)):
                        i_valeur = y + int(y_coo[z]) # Prise des coordonnées x et y pour ensuite pouvoir calculer les coordonnées alentours
                        x_valeur = x + int(x_coo[z])

                        # Méthode pour dévoiler les cases optimisée tiré d'une vidéo
                        if i_valeur >= 0 and i_valeur < self.haut and x_valeur >= 0 and x_valeur < self.long:
                            if self.grille[i_valeur][x_valeur]["relief"] != "sunken":
                                JeuSolo.click_gauche(self, i_valeur, x_valeur)

                if self.score_solo == self.score_solo_final: # Conditions pour gagner en fonction du score clacluer à chaque case dévoilée
                    self.fenetre_gagner = Tk() # Création d'une nouvelle fenêtre pour annoncer que la partie est gagnée
                    self.message_gagner = Label(self.fenetre_gagner, text="Vous avez gagné !!!")
                    self.message_gagner.grid()
                    self.tout_quitter = Button(self.fenetre_gagner, text="Quitter Démineur",command=self.fenetre_demineur.destroy)
                    self.tout_quitter.grid()
                    self.fenetre_gagner.mainloop()
                    quit() # On utilise quit() pour arreter le programme en arrière plan
                    # car les boutons(enfin plutot Tkinter) agissent comme une boucle while

            else:
                self.grille[y][x].configure(bg="Red", text="*")
                for a in range(len(self.grille)):
                    for b in range(len(self.grille[a])):
                        if self.grille[a][b].mine == "True":
                            if self.grille[a][b]["text"] == "D":
                                self.grille[a][b].configure(bg="Green")
                            elif self.grille[a][b]["bg"] != "Red":
                                self.grille[a][b].configure(bg="Pink", text="*")

                        elif self.grille[a][b]["text"] == "D":
                            self.grille[a][b].configure(bg="Yellow")
                self.fenetre_perdue = Tk()  # Création d'une nouvelle fenêtre pour annoncer que la partie est perdue
                self.message_perdue = Label(self.fenetre_perdue, text="Vous avez perdue !!!")
                self.message_perdue.grid()
                self.tout_quitter = Button(self.fenetre_perdue, text="Quitter Démineur",
                                       command=self.fenetre_demineur.destroy)
                self.tout_quitter.grid()
                self.fenetre_perdue.mainloop()
                quit()  # On utilise quit() pour arreter le programme en arrière plan
                # car les boutons(enfin plutot Tkinter) agissent comme une boucle while

    def clic_droit(self, cd_presser, i, x):
        """
        Change le nom des boutons pour poser un drapeau en fonction de l'évènement bouton 3 soit le clic droit
        """
        if self.grille[i][x]["relief"] != "sunken": # Si le bouton n'est pas "enfoncé"
            if self.grille[i][x]["text"] == "":
                self.grille[i][x].config(text="D") # alors on affiche un D pour drapeau lors du clic droit
            else:
                self.grille[i][x].config(text="")


def lancer_partie_solo():
    """
    Fonction toute simple pour lancer la partie démineur solo et fermer la fen^tre principale
    """
    main_windows.destroy()
    JeuSolo()
    quit()

lancer()
