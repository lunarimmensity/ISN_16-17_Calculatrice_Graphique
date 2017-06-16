# -*- coding:UTF-8 -*-

import math
import os
import time
import tkinter.messagebox
import turtle
import tkinter
from random import randint


def bouton_off(fValeurs):
    # erregistrement des valeurs du thème

    fichier = open("color.txt", 'w')
    fichier.write("bouton \n")
    fichier.write(fValeurs.get("col_btn"))
    fichier.write("\n \nfond \n")
    fichier.write(fValeurs.get("col_bg"))
    fichier.write("\n \nbordure \n")
    fichier.write(fValeurs.get("col_cadre"))
    fichier.write("\n \ncrayon \n")
    fichier.write(fValeurs.get("col_crayon"))
    fichier.write("\n \nrelief\n")
    fichier.write(fValeurs.get("relief"))
    fichier.close()

    # fermeture de la calculatrice
    fValeurs["dyna"] = False
    calc.destroy()


def bouton_ac(fValeurs, fL_fonctions, fFonctions):
    # réinitialisation de la fonction

    # effacage de la courbe
    fValeurs["dyna"] = False
    time.sleep(0.5)
    courbe.clear()

    # effacage de l'expression
    for i in fL_fonctions:
        i.destroy()

    fL_fonctions.clear()
    fFonctions.clear()


def bouton_nouveau(lieu):
    def setTab(fLieu, tab, valeur):
        if len(fLieu) >= 2:
            setTab(fLieu[-len(fLieu) + 1:], tab[fLieu[0]], valeur)
        else:
            tab[fLieu[0]] = valeur

    def traitement(entree):
        # traite l'entrée des boites de dialogue
        a = None

        if entree == 'x' or entree == 'a':
            a = entree

        elif entree == "fonc":
            pass
        else:
            try:
                a = int(entree)
            except TypeError and ValueError:
                tkinter.messagebox.showerror(
                    "EXPRESSION INCORRECTE",
                    "l'expression peut etre un :\n\t- un réel\n\t-a\n\t-x\n\t-une sous fonction")
        return a

    def boite_de_dialogue2(func, nb1, nb2, titre, symb):
        # assigne à la suite d'operations le calcul à faire

        def plus(fLieu, rang):
            if rang == 1:
                v_nb_1.set("fonc")
            else:
                v_nb_2.set("fonc")
            enrregistrer(fLieu)
            l = fLieu.copy()
            l.append(rang)

            bouton_nouveau(l)

        def enrregistrer(fLieu):
            a = traitement(v_nb_1.get())

            b = traitement(v_nb_2.get())

            setTab(fLieu, fonctions, [func, a, b, symb])

        def ok(fLieu):
            if v_nb_1.get() != "fonc" and v_nb_2.get() != "fonc":
                enrregistrer(fLieu)
            dialogue.destroy()

        dialogue = tkinter.Toplevel(calc)
        dialogue.title(titre)

        fen_clavier.destroy()

        tkinter.Label(dialogue, text=nb1).pack()

        v_nb_1 = tkinter.StringVar()
        tkinter.Entry(dialogue, textvariable=v_nb_1).pack()
        tkinter.Button(dialogue, text='✚', command=lambda fLieu=lieu: plus(fLieu, 1), bg=valeurs.get("col_btn")
                       ).pack()

        tkinter.Label(dialogue, text=nb2).pack()

        v_nb_2 = tkinter.StringVar()
        tkinter.Entry(dialogue, textvariable=v_nb_2).pack()

        tkinter.Button(dialogue, text='✚', command=lambda fLieu=lieu: plus(fLieu, 2), bg=valeurs.get("col_btn")
                       ).pack()
        tkinter.Button(dialogue, text="OK", command=lambda fLieu=lieu: ok(fLieu), bg=valeurs.get("col_btn")).pack()

        dialogue.mainloop()

    def boite_de_dialogue1(func, nb1, titre, symb):
        # assigne à la suite d'operations le calcul à faire

        def plus(fLieu):
            v_nb.set("fonc")
            enrregistrer(fLieu)
            l = fLieu.copy()
            l.append(1)

            bouton_nouveau(l)

        def enrregistrer(fLieu):
            a = traitement(v_nb.get())

            setTab(fLieu, fonctions, [func, a, symb])

        def ok(fLieu):
            if v_nb.get() != "fonc":
                enrregistrer(fLieu)
            dialogue.destroy()

        dialogue = tkinter.Toplevel(calc)
        dialogue.title(titre)

        fen_clavier.destroy()

        tkinter.Label(dialogue, text=nb1).pack()
        v_nb = tkinter.StringVar()
        tkinter.Entry(dialogue, textvariable=v_nb).pack()

        tkinter.Button(dialogue, text='✚', command=lambda fLieu=lieu: plus(fLieu), bg=valeurs.get("col_btn")).pack()
        tkinter.Button(dialogue, text="OK", command=lambda fLieu=lieu: ok(fLieu), bg=valeurs.get("col_btn")).pack()
        dialogue.mainloop()

    boutons = [
        [["pow", lambda: boite_de_dialogue2(math.pow, 'Nombre', 'Exposant', 'Puissance', 'pow')],
         ["E",
          lambda:  (lambda a, b: a * math.pow(10, b), 'Nombre :', 'puissance :', 'Puissance de 10 :',
                                     'E^')]],
        [["tan⁻¹", lambda: boite_de_dialogue1(math.atan, "Nombre", "arc tangente", 'tan⁻¹')],
         ["log", lambda: boite_de_dialogue1(lambda x: math.log(x, 10), "Nombre", "logarithme", 'log')]],
        [["sin⁻¹", lambda: boite_de_dialogue1(math.asin, "Nombre", "arc sinus", 'sin⁻¹')],
         ["cos⁻¹", lambda: boite_de_dialogue1(math.acos, "Nombre", "arc cosinus", 'cos⁻¹')]],
        [["sin", lambda: boite_de_dialogue1(math.sin, "Nombre", "sinus", 'sin')],
         ["cos", lambda: boite_de_dialogue1(math.cos, "Nombre", "cosinus", 'cos')]],
        [["exp", lambda: boite_de_dialogue1(math.exp, 'Nombre', 'Exponentielle', 'e^')],
         ["tan", lambda: boite_de_dialogue1(math.tan, "Nombre", "tangente", 'tan')]],
        [["sqrt", lambda: boite_de_dialogue1(math.sqrt, 'Nombre', 'Racine', '√')],
         ["ln", lambda: boite_de_dialogue1(lambda x: math.log(x, math.e), 'Nombre', 'logarithme néperien', 'ln')]],
        [["+", lambda: boite_de_dialogue2(lambda a, b: a + b, 'Nombre 1:', 'Nombre 2:', 'Somme', '+')],
         ["×", lambda: boite_de_dialogue2(lambda a, b: a * b, 'Nombre 1:', 'Nombre 2:', 'Multiplication', '×')]],
        [['-', lambda: boite_de_dialogue2(lambda a, b: a - b, 'Nombre 1:', 'Nombre 2:', 'Soustraction', '-')],
         ['÷', lambda: boite_de_dialogue2(lambda a, b: a / b, 'Numerateur', 'Denominateur', 'Division', '÷')]],
    ]

    fen_clavier = tkinter.Toplevel(calc)
    fen_clavier.title("nouvelle expression")

    # affichage des boutons
    for i in range(len(boutons)):
        for j in range(len(boutons[i])):
            tkinter.Button(fen_clavier, text=boutons[i][j][0], relief="flat", command=boutons[i][j][1], height=1,
                           width=4, bg=valeurs.get("col_btn")).grid(row=i, column=j, padx=2, pady=2)

    fen_clavier.mainloop()


# def test():
#     # fonction testeuse pour btn test
#     pass


def executer(fValeurs):
    afficher_expressions()
    # lance le calcul/tracer
    if l_mode["text"] == "Calculatrice":

        # efacage de la courbe et des axes
        courbe.clear()
        axes.clear()

        # renime a 0 de la tortue courbe
        clearT(courbe)
        courbe.up()
        courbe.goto(0, 0)
        # ecriture de l'expression
        courbe.left(90)
        for i in range(len(l_foctions)):
            courbe.write(l_foctions[i]["text"] + " = ", move=True)

            # ecriture du resultat (ou erreur)
            resultat = None
            try:
                resultat = calcul(fonctions[i])

            except Exception as e:
                tkinter.messagebox.showerror("ERREUR DANS LE CALCUL", "Une erreur est survenue:\n\n« " + str(e) + " »")
                resultat = "ERREUR"
                print(e)
            finally:
                # écriture duresultat
                courbe.write(resultat)
            courbe.fd(30)



    elif l_mode["text"] == "Grapheur":
        courbe.clear()
        setT(courbe)
        for i in fonctions:
            tracer_graphe(i)
            courbe.color(set_couleur(randint(0, 255), randint(0, 255), randint(0, 255)))

    elif l_mode["text"] == "Dynamique":

        # lance le grapheur dynamique
        fValeurs["dyna"] = True

        # tant que mode dyna activé trace courbe attend
        a = fValeurs.get("aMin")
        while fValeurs.get("dyna"):
            if a > fValeurs.get("aMax"):
                a = fValeurs.get("aMin")
            for i in fonctions:
                tracer_graphe(i, a, True)
            time.sleep(fValeurs.get("pause"))
            a += fValeurs.get("pas")


# param ds menu
def menu_repere():
    # fonction permettant de règler la fenêtre graphique

    def ok():

        # verifie coherence des valeurs
        if float(v_xMin.get()) >= float(v_xMax.get()):
            tkinter.messagebox.showerror("ERREUR DE PLAGE EN x",
                                         "les valeurs min et max doivent etre dans l'ordre et différentes")
        else:
            valeurs["xMin"] = float(v_xMin.get())
            valeurs["xMax"] = float(v_xMax.get())

        if float(v_yMin.get()) >= float(v_yMax.get()):
            tkinter.messagebox.showerror("ERREUR DE PLAGE EN y",
                                         "les valeurs min et max doivent etre dans l'ordre et différentes")
        else:
            # erregistre les valeurs si pas de pb
            valeurs["yMin"] = float(v_yMin.get())
            valeurs["yMax"] = float(v_yMax.get())

        # erregistre les pas si sont positif
        if float(v_xPas.get()) > 0:
            valeurs["xPas"] = float(v_xPas.get())
        else:
            tkinter.messagebox.showerror("ERREUR DE PAS", "le pas en x doit être superieur à 0")

        if float(v_yPas.get()) > 0:
            valeurs["yPas"] = float(v_xPas.get())
        else:
            tkinter.messagebox.showerror("ERREUR DE PAS", "le pas en y doit être superieur à 0")

        actualiser(valeurs)
        # actualise la fenêtre
        if l_mode['text'] == 'Grapheur' or l_mode['text'] == 'Dynamique':
            axes.clear()
            tracer_axes()
        fen_repere.destroy()
        courbe.clear()

    # déclaration de la fenêtre
    fen_repere = tkinter.Toplevel(calc)
    fen_repere.title("repère")

    # déclaration des labels
    l_xMin = tkinter.Label(fen_repere, text="x min")
    l_xMax = tkinter.Label(fen_repere, text="x max")
    l_yMin = tkinter.Label(fen_repere, text="y min")
    l_yMax = tkinter.Label(fen_repere, text="y max")
    l_xpas = tkinter.Label(fen_repere, text="pas x")
    l_ypas = tkinter.Label(fen_repere, text="pas y")

    # déclaration des entrées et de leurs labels
    v_xMin = tkinter.StringVar()
    v_xMin.set(str(valeurs.get("xMin")))
    e_xMin = tkinter.Entry(fen_repere, textvariable=v_xMin)

    v_xMax = tkinter.StringVar()
    v_xMax.set(str(valeurs.get("xMax")))
    e_xMax = tkinter.Entry(fen_repere, textvariable=v_xMax)

    v_yMin = tkinter.StringVar()
    v_yMin.set(str(valeurs.get("yMin")))
    e_yMin = tkinter.Entry(fen_repere, textvariable=v_yMin)

    v_yMax = tkinter.StringVar()
    v_yMax.set(str(valeurs.get("yMax")))
    e_yMax = tkinter.Entry(fen_repere, textvariable=v_yMax)

    v_xPas = tkinter.StringVar()
    v_xPas.set(str(valeurs.get("xPas")))
    e_xPas = tkinter.Entry(fen_repere, textvariable=v_xPas)

    v_yPas = tkinter.StringVar()
    v_yPas.set(str(valeurs.get("yPas")))
    e_yPas = tkinter.Entry(fen_repere, textvariable=v_yPas)

    # affichage
    l_xMin.grid(column=1, row=1, padx=2, pady=2)
    e_xMin.grid(column=1, row=2, padx=2, pady=2)
    l_yMin.grid(column=1, row=3, padx=2, pady=2)
    e_yMin.grid(column=1, row=4, padx=2, pady=2)
    l_xMax.grid(column=2, row=1, padx=2, pady=2)
    e_xMax.grid(column=2, row=2, padx=2, pady=2)
    l_yMax.grid(column=2, row=3, padx=2, pady=2)
    e_yMax.grid(column=2, row=4, padx=2, pady=2)
    l_xpas.grid(column=3, row=1, padx=2, pady=2)
    e_xPas.grid(column=3, row=2, padx=2, pady=2)
    l_ypas.grid(column=3, row=3, padx=2, pady=2)
    e_yPas.grid(column=3, row=4, padx=2, pady=2)
    tkinter.Button(fen_repere, text="ok", command=ok, bg=valeurs.get("col_btn")).grid(row=5, column=2, padx=2, pady=2)


def menu_dyna():
    # fonction permettant de règler la fenêtre dynamique

    def ok():
        if float(v_amin.get()) >= float(v_amax.get()):
            tkinter.messagebox.showerror("ERREUR PLAGE", "a max doit être strictement superieur à a min")
        else:
            valeurs["aMin"] = float(v_amin.get())
            valeurs["aMax"] = float(v_amax.get())
        if float(v_pas.get()) <= 0:
            tkinter.messagebox.showerror("VALEUR INCORRECTE", "le pas doit être srictement supperieur à 0")
        else:
            valeurs["pas"] = float(v_pas.get())
        if float(v_pause.get()) <= 0:
            tkinter.messagebox.showerror("VALEUR INCORRECTE", "la pause doit être strictement superieure à 0")
        valeurs["pause"] = float(v_pause.get())
        fen_dyna.destroy()

    # déclaration de la fenêtre
    fen_dyna = tkinter.Toplevel(calc)
    fen_dyna.title("paramètres de la fenêtre dynamique")

    # déclaration des labels
    l_aMin = tkinter.Label(fen_dyna, text="a min")
    l_aMax = tkinter.Label(fen_dyna, text="a max")
    l_pas = tkinter.Label(fen_dyna, text="pas")
    l_pause = tkinter.Label(fen_dyna, text="pause")

    # déclaration des variables des entrées
    v_amin = tkinter.StringVar()
    v_amin.set(str(valeurs.get("aMin")))
    v_amax = tkinter.StringVar()
    v_amax.set(str(valeurs.get("aMax")))
    v_pas = tkinter.StringVar()
    v_pas.set(str(valeurs.get("pas")))
    v_pause = tkinter.StringVar()
    v_pause.set(valeurs.get("pause"))

    # déclaration des entrées
    e_aMin = tkinter.Entry(fen_dyna, textvariable=v_amin)
    e_aMax = tkinter.Entry(fen_dyna, textvariable=v_amax)
    e_pas = tkinter.Entry(fen_dyna, textvariable=v_pas)
    e_pause = tkinter.Entry(fen_dyna, textvariable=v_pause)

    # affichage
    l_aMin.grid(column=1, row=1)
    e_aMin.grid(column=1, row=2)
    l_aMax.grid(column=2, row=1)
    e_aMax.grid(column=2, row=2)
    l_pas.grid(column=1, row=3)
    e_pas.grid(column=1, row=4)
    l_pause.grid(column=2, row=3)
    e_pause.grid(column=2, row=4)
    tkinter.Button(fen_dyna, text="ok", command=ok, bg=valeurs.get("col_btn")).grid(column=1, row=5)


def couleur():
    # fonction permettant de paramètrer les couleurs

    def ok():
        if b_titre['text'] == labels[0]:  # boutons
            valeurs["col_btn"] = set_couleur(rouge.get(), vert.get(), bleu.get())
            b_ac['bg'] = valeurs.get("col_btn")
            b_titre['bg'] = valeurs.get("col_btn")
            b_executer['bg'] = valeurs.get("col_btn")
            b_nouveau['bg'] = valeurs.get("col_btn")
            b_off['bg'] = valeurs.get("col_btn")

        elif b_titre['text'] == labels[1]:
            valeurs["col_bg"] = set_couleur(rouge.get(), vert.get(), bleu.get())
            f_commande['bg'] = valeurs.get("col_bg")
            f_clavier['bg'] = valeurs.get("col_bg")
            calc['bg'] = valeurs.get("col_bg")
            lf_expression['bg'] = valeurs.get("col_bg")
            l_foctions[- 1]['bg'] = valeurs.get("col_bg")
        elif b_titre['text'] == labels[2]:
            valeurs["col_cadre"] = set_couleur(rouge.get(), vert.get(), bleu.get())
            l_mode['bg'] = valeurs["col_cadre"]
            f_turtle['bg'] = valeurs["col_cadre"]
        elif b_titre['text'] == labels[3]:
            valeurs["col_crayon"] = set_couleur(rouge.get(), vert.get(), bleu.get())
        fen_couleur.destroy()

    def voir():
        b_voir["bg"] = set_couleur(rouge.get(), vert.get(), bleu.get())

    def defiler_elements():
        a = labels.index(b_titre['text'])
        if a >= len(labels) - 1:
            b_titre['text'] = labels[0]
        else:
            b_titre['text'] = labels[a + 1]

    labels = ['boutons', 'fond', 'cadre', 'crayon']
    fen_couleur = tkinter.Toplevel(calc)
    fen_couleur.title("Couleur")

    b_titre = tkinter.Button(fen_couleur, text=labels[0], command=defiler_elements, bg=valeurs.get("col_btn"))
    rouge = tkinter.IntVar()
    rouge.set(0)
    vert = tkinter.IntVar()
    vert.set(0)
    bleu = tkinter.IntVar()
    bleu.set(255)

    scl_rouge = tkinter.Scale(fen_couleur, variable=rouge, from_=0, to=255, label="rouge", orient="horizontal")
    scl_vert = tkinter.Scale(fen_couleur, variable=vert, from_=0, to=255, label="vert", orient="horizontal")
    scl_bleu = tkinter.Scale(fen_couleur, variable=bleu, from_=0, to=255, label="bleu", orient="horizontal")
    b_voir = tkinter.Button(fen_couleur, text="prévisualiser", command=voir, bg=valeurs.get("col_btn"))

    b_titre.pack()
    scl_rouge.pack()
    scl_vert.pack()
    scl_bleu.pack()
    b_voir.pack()
    voir()
    tkinter.Button(fen_couleur, text="OK", command=ok, bg=valeurs.get("col_btn")).pack(side="bottom")


def relief():
    reliefs = ["flat", "raised", "solid", "groove", "ridge", "sunken"]

    def click():

        i = reliefs.index(b_relief['text'])

        if i < len(reliefs) - 1:
            i += 1
        else:
            i = 0
        b_relief['text'] = reliefs[i]
        b_relief['relief'] = reliefs[i]

    def ok():
        valeurs["relief"] = b_relief["text"]
        b_off["relief"] = valeurs.get("relief")
        b_nouveau["relief"] = valeurs.get("relief")
        b_executer["relief"] = valeurs.get("relief")
        b_ac["relief"] = valeurs.get("relief")
        fen_relief.destroy()

    fen_relief = tkinter.Toplevel(calc)
    fen_relief.title("relief")
    b_relief = tkinter.Button(fen_relief, text=reliefs[0], relief=reliefs[0], command=click, bg=valeurs.get("col_btn"))
    b_relief.pack()
    b_ok = tkinter.Button(fen_relief, text="OK", relief=valeurs.get("relief"), command=ok, bg=valeurs.get("col_btn"))
    b_ok.pack()


def menu_pen():
    # fonction permettant de paramètrer le crayon

    def ok():
        if float(v_epaiseur.get()) <= 0:
            tkinter.messagebox.showerror("VALEUR INCORRECTE", "l'épaisseur doit être strictement positive")
        else:
            valeurs["epaisseur"] = float(v_epaiseur.get())
        if float(v_precision.get()) <= 0:
            tkinter.messagebox.showerror("VALEUR INCORRECTE", "la precision doit être strictement superieure à 0")
        else:
            valeurs["precision"] = float(v_precision.get())
        fen_pen.destroy()

    fen_pen = tkinter.Toplevel(calc)
    fen_pen.title("paramètres du crayon")

    f_reste = tkinter.Frame(fen_pen)
    f_reste.pack(side="right")

    l_epaisseur = tkinter.Label(f_reste, text="épaisseur")
    l_precision = tkinter.Label(f_reste, text="l_precision")

    v_epaiseur = tkinter.StringVar()
    v_epaiseur.set(str(valeurs.get("epaisseur")))
    v_precision = tkinter.StringVar()
    v_precision.set(str(valeurs.get("precision")))

    e_epaisseur = tkinter.Entry(f_reste, textvariable=v_epaiseur)
    e_precision = tkinter.Entry(f_reste, textvariable=v_precision)

    l_epaisseur.pack()
    e_epaisseur.pack()
    l_precision.pack()
    e_precision.pack()
    tkinter.Button(fen_pen, text="OK", command=ok, bg=valeurs.get("col_btn")).pack(side="bottom")


def mode_calc():
    # met la calculatrice en mode calcul
    ecran.clear()
    l_mode["text"] = "Calculatrice"
    valeurs["dyna"] = False


def mode_graph():
    # met la calculatrice en mode grapheur
    ecran.clear()
    axes.seth(0)
    axes.clear()
    axes.pd()
    tracer_axes()
    l_mode["text"] = "Grapheur"
    valeurs["dyna"] = False


def mode_dyna():
    # met la calculatrice en mode grapheur dynamique
    ecran.clear()
    tracer_axes()
    l_mode["text"] = "Dynamique"
    valeurs["dyna"] = True


def afficher_expressions():
    def fonctionToString(tab):
        if len(tab) == 3:
            if isinstance(tab[1], list):
                chaine = tab[2] + " ( " + fonctionToString(tab[1]) + " )"
            else:
                chaine = tab[2] + " " + str(tab[1])
        else:
            if isinstance(tab[1], list):
                a = " ( " + fonctionToString(tab[1]) + " )"
            else:
                a = str(tab[1])
            if isinstance(tab[2], list):
                b = " ( " + fonctionToString(tab[2]) + " )"
            else:
                b = str(tab[2])
            chaine = a + " " + tab[3] + " " + b

        return chaine

    for i in range(len(fonctions)):
        l_foctions.append(tkinter.Label(lf_expression, text=fonctionToString(fonctions[i]), bg=valeurs.get("col_bg")))
        l_foctions[i].pack(padx=2, pady=2)


def calcul(tab, x=0, a=0):
    def traitement(rang, fTab):
        if isinstance(fTab[rang], list):
            fNb = calcul(fTab[rang], x, a)
        elif fTab[rang] == "x":
            fNb = x
        elif fTab[rang] == "a":
            fNb = a
        else:
            fNb = fTab[rang]
        return fNb

    if len(tab) == 3:
        nb = traitement(1, tab)
        return tab[0](nb)
    else:
        nb_1 = traitement(1, tab)
        nb_2 = traitement(2, tab)
        return tab[0](nb_1, nb_2)


# fonctions de coordonées

def coord(x, de_min, de_max, a_min, a_max):
    de_diff = de_max - de_min
    a_diff = a_max - a_min
    assert de_diff != 0, "Les valeurs d'orrigine min et max doivent etres ≠"
    assert a_diff != 0, "Les valeurs d'arrivée min et max doivent etres ≠"
    return (a_diff / de_diff) * (x - de_min) - a_diff // 2


def coords(x, y, de_xmin, de_xmax, a_xmin, a_xmax, de_ymin, de_ymax, a_ymin, a_ymax):
    # retuorne les cocrdonnées de la fen à partir de celles du repère

    return coord(x, de_xmin, de_xmax, a_xmin, a_xmax), coord(y, de_ymin, de_ymax, a_ymin, a_ymax)


# paramètres de la tortue
def clearT(tortue):
    tortue.clear()
    tortue.pencolor("black")
    tortue.width(1)
    tortue.seth(0)
    tortue.ht()
    tortue.fillcolor("black")
    ecran.tracer(20, 25)


def setT(tortue):
    tortue.color(valeurs.get("col_crayon"))
    tortue.width(valeurs.get("epaisseur"))
    tortue.up()


# tracer graphiques

def tracer_axes():
    def fleche():
        axes.fd(5)
        axes.begin_fill()
        axes.left(90)
        axes.fd(4)
        axes.right(135)
        axes.fd(4 * 2 ** 0.5)
        axes.right(90)
        axes.fd(4 * 2 ** 0.5)
        axes.right(135)
        axes.fd(4)
        axes.end_fill()

    def axex():
        def graduation(fA):
            if fA % valeurs.get("xPas") == 0:
                axes.right(90)
                axes.fd(2)
                if fA != 0:
                    axes.up()
                    axes.fd(20)
                    axes.write(fA, align='center')
                    axes.bk(20)
                    axes.pd()
                axes.bk(4)
                axes.fd(2)
                axes.left(90)

        a = valeurs.get("xMin")
        while axes.xcor() < valeurs.get("xUtilFen") // 2:
            axes.setx(
                coord(a, valeurs.get("xMin"), valeurs.get("xMax"), -valeurs.get("xFenMax"), valeurs.get("xFenMax")))
            graduation(a)
            a += 1
        # flèche bout axe
        fleche()
        axes.up()

    def axey():
        def graduation(fA):
            if fA % valeurs.get("yPas") == 0:
                axes.right(90)
                axes.fd(2)
                if fA != 0:
                    axes.up()
                    axes.fd(20)
                    axes.write(fA, align='center')
                    axes.bk(20)
                    axes.pd()
                axes.bk(4)
                axes.fd(2)
                axes.left(90)

        a = valeurs.get("yMin")
        while axes.ycor() < valeurs.get("yUtilFen") // 2:
            axes.sety(
                coord(a, valeurs.get("yMin"), valeurs.get("yMax"), -valeurs.get("yFenMax"), valeurs.get("yFenMax")))
            graduation(a)
            a += 1
        # flèche bout axe
        fleche()
        axes.up()

    clearT(axes)
    axes.up()

    # tracer axe des x
    if valeurs.get("yMin") > 0:
        axes.goto(
            coords(valeurs.get("xMin"), valeurs.get("yMin"), de_xmin=valeurs.get("xMin"),
                   de_xmax=valeurs.get("xMax"), a_xmin=-valeurs.get("xFenMax"), a_xmax=valeurs.get("xFenMax"),
                   de_ymin=valeurs.get("yMin"),
                   de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
        axes.down()
        axex()
    elif valeurs.get("yMax") < 0:
        axes.goto(
            coords(valeurs.get("xMin"), valeurs.get("yMax"), de_xmin=valeurs.get("xMin"),
                   de_xmax=valeurs.get("xMax"), a_xmin=-valeurs.get("xFenMax"), a_xmax=valeurs.get("xFenMax"),
                   de_ymin=valeurs.get("yMin"),
                   de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
        axes.down()
        axex()
    else:
        axes.goto(
            coords(valeurs.get("xMin"), 0, de_xmin=valeurs.get("xMin"), de_xmax=valeurs.get("xMax"),
                   a_xmin=-valeurs.get("xFenMax"), a_xmax=valeurs.get("xFenMax"), de_ymin=valeurs.get("yMin"),
                   de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
        axes.down()
        axex()

    # tracer axe des y
    if valeurs.get("xMin") > 0:
        axes.goto(
            coords(valeurs.get("xMin"), valeurs.get("yMin"), de_xmin=valeurs.get("xMin"),
                   de_xmax=valeurs.get("xMax"), a_xmin=-valeurs.get("xFenMax"), a_xmax=valeurs.get("xFenMax"),
                   de_ymin=valeurs.get("yMin"),
                   de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
        axes.down()
        axey()
    elif valeurs.get("xMax") < 0:
        axes.goto(
            coords(valeurs.get("xMax"), valeurs.get("yMin"), de_xmin=valeurs.get("xMin"),
                   de_xmax=valeurs.get("xMax"),
                   a_xmin=-valeurs.get("xFenMax"), a_xmax=valeurs.get("xFenMax"),
                   de_ymin=valeurs.get("yMin"),
                   de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
        axes.down()
        axey()
    else:
        axes.goto(
            coords(0, valeurs.get("yMin"), de_xmin=valeurs.get("xMin"), de_xmax=valeurs.get("xMax"),
                   a_xmin=-valeurs.get("xFenMax"), a_xmax=valeurs.get("xFenMax"), de_ymin=valeurs.get("yMin"),
                   de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
        axes.down()
        axey()
    axes.up()


def tracer_graphe(fonc, a=0, afficherA=False):
    clearT(courbe)

    setT(courbe)
    g = valeurs.get("xMin")
    while g <= valeurs.get("xMax"):

        try:
            courbe.goto(
                coords(g, calcul(fonc, x=g, a=a), de_xmin=valeurs.get("xMin"), de_xmax=valeurs.get("xMax"),
                       a_xmin=-valeurs.get("xFenMax"),
                       a_xmax=valeurs.get("xFenMax"),
                       de_ymin=valeurs.get("yMin"),
                       de_ymax=valeurs.get("yMax"), a_ymin=-valeurs.get("yFenMax"), a_ymax=valeurs.get("yFenMax")))
            courbe.pd()
        except ValueError:
            courbe.up()

        g += valeurs.get("precision")
    courbe.up()
    if afficherA:
        courbe.goto(valeurs.get("xUtilFen") // 2 - 100, -valeurs.get("yUtilFen") // 2)
        courbe.write("a= " + str(a))


def set_couleur(r, v, b):
    r = hex(r)
    v = hex(v)
    b = hex(b)
    s = "#"
    try:
        s += r[2] + r[3]
    except IndexError:
        s += "0" + r[2]

    try:
        s += v[2] + v[3]
    except IndexError:
        s += "0" + v[2]
    try:
        s += b[2] + b[3]
    except IndexError:
        s += "0" + b[2]
    return s


def actualiser(fValeurs):
    fValeurs["xDiff"] = fValeurs.get("xMax") - fValeurs.get("xMin")
    fValeurs["yDiff"] = fValeurs.get("yMax") - fValeurs.get("yMin")
    fValeurs["xUtilFen"] = fValeurs.get("xFen") - 2 * fValeurs.get("marges")
    fValeurs["yUtilFen"] = fValeurs.get("yFen") - 2 * fValeurs.get("marges")
    fValeurs["xFenMax"] = fValeurs.get("xFen") // 2 - fValeurs.get("marges")
    fValeurs["yFenMax"] = fValeurs.get("yFen") // 2 - fValeurs.get("marges")


def nouvelleFonction(fFonctions):
    fFonctions.append(None)
    bouton_nouveau([-1])


def chargement(fValeurs):
    chemin = "color.txt"
    if os.path.exists(chemin):
        fichier = open(chemin, 'r')
        fichier.readline()
        fValeurs["col_btn"] = fichier.readline()[:-1]
        fichier.readline()
        fichier.readline()
        fValeurs["col_bg"] = fichier.readline()[:-1]
        fichier.readline()
        fichier.readline()
        fValeurs["col_cadre"] = fichier.readline()[:-1]


fonctions = []
l_foctions = []

valeurs = {
    "xFen": 800,
    "yFen": 500,
    "marges": 30,
    "dyna": False,
    "xMin": -5,
    "xMax": 5,
    "xPas": 1,
    "yMin": -5,
    "yMax": 5,
    "yPas": 1,
    "epaisseur": 5,
    "precision": 0.005,
    "aMin": -5,
    "aMax": 5,
    "aPas": 1,
    "pause": 1,
    "col_btn": "grey",
    "col_bg": "white",
    "col_cadre": "black",
    "col_crayon": "blue",
    "relief": "flat"

}

actualiser(valeurs)

chargement(valeurs)

# déclaration de la fenêtre
calc = tkinter.Tk()
calc.title("Calcultrice")
calc.configure(bg="white")

# déclaration et affichage des frames
f_commande = tkinter.Frame(calc, relief="ridge", bg=valeurs.get("col_bg"))
f_clavier = tkinter.Frame(f_commande, relief="ridge", bg=valeurs.get("col_bg"))
f_turtle = tkinter.Frame(calc, relief="ridge", bg=valeurs.get("col_cadre"))

f_commande.pack(side="left")
f_turtle.pack(side="right")

# déclaration et affichage du label modedans le label tortue
mode = "Calculatrice"
l_mode = tkinter.Label(f_turtle, text=mode, bg=valeurs.get("col_cadre"), fg="white")
l_mode.pack()

# déclaratior et affichage de la frame entrée
lf_expression = tkinter.LabelFrame(f_commande, text="entrée", bg=valeurs.get("col_bg"))
lf_expression.pack(padx=2, pady=2)

# déclaration et affichage de la tortue
fenTortue = turtle.Canvas(f_turtle, height=valeurs.get("yFen"), width=valeurs.get("xFen"))
fenTortue.pack(padx=10, pady=10)
ecran = turtle.TurtleScreen(fenTortue)
ecran.tracer(20, 25)
courbe = turtle.RawTurtle(ecran)
axes = turtle.RawTurtle(ecran)
courbe.ht()
axes.ht()

# barre de menu
menu = tkinter.Menu(calc)

mode = tkinter.Menu(menu, tearoff=0)
mode.add_command(label="Calculatrice", command=mode_calc)
mode.add_command(label="Grapheur", command=mode_graph)
mode.add_command(label="Grapheur Dynamique", command=mode_dyna)

menu.add_cascade(label='Mode', menu=mode)

parametres = tkinter.Menu(menu, tearoff=0)
parametres.add_command(label="Fenêtre graphique", command=menu_repere)
parametres.add_command(label="Dynamique", command=menu_dyna)
parametres.add_command(label="Crayon", command=menu_pen)
parametres.add_separator()
parametres.add_command(label="changer de couleur", command=couleur)
parametres.add_command(label="changer de reliefs (boutons)", command=relief)
menu.add_cascade(label="pamètres", menu=parametres)

calc.config(menu=menu)

# declaration des boutons:

b_off = tkinter.Button(f_commande, text="OFF", command=lambda fValeurs=valeurs: bouton_off(fValeurs), height=1, width=4,
                       bg=valeurs.get("col_btn"))
b_ac = tkinter.Button(f_commande, text="AC",
                      command=lambda fValeurs=valeurs: bouton_ac(fValeurs, l_foctions, fonctions), height=1,
                      width=4,
                      bg=valeurs.get("col_btn"))
b_nouveau = tkinter.Button(f_commande, text="✚", command=lambda x=fonctions: nouvelleFonction(fonctions), height=1,
                           width=4,
                           bg=valeurs.get("col_btn"))
b_executer = tkinter.Button(f_commande, text="⏎", command=lambda fValeurs=valeurs: executer(fValeurs), height=1,
                            width=4, bg=valeurs.get("col_btn"))
# b_test = tkinter.Button(f_commande, text="test", command=test, height=1, width=4, bg=valeurs.get("col_btn"))

b_nouveau.pack()
b_off.pack()
b_ac.pack()
b_executer.pack()
# b_test.pack()



# afichage de la fenetre
calc.mainloop()
