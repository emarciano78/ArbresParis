#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eric
#
# Created:     12/06/2019
# Copyright:   (c) eric 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Lien en Francais sur Tkinter --> http://tkinter.fdex.eu/index.html

import pandas as pd               # Pandas
import matplotlib.pyplot as plt   # Pour faire les graphiques (installer via pip)
#import numpy as np
import csv

import easygui as g
#from IPython.display import display,HTML # Pour afficher les dataframes en pages HTML sous Jupyter
from tabulate import tabulate      # Permet d'afficher des dataframe en mode texte (pip install tabulate)
from gmplot import *               # Gestion de GMAP (API)
import os                          # pour effacer les fichiers temporaires des graphiques
from ipywidgets.embed import embed_minimal_html  # Pour exporter en HTML

from tkinter import *       # Importation du module Tkinter
                            # Ce module est déjà intégré à Python 3
import tkinter.ttk as ttk   # Ajout plus de Widgets (ComboBox)
from PIL import Image, ImageTk # Pour les images
from tk_html_widgets import HTMLLabel # Pour l'HTML
import webbrowser           # Pour afficher le GMAP HTML
import datetime

def retourne_DF_filtre(gmap=False):
    """
        Retourne un DF filté suivant la selection de l'utilisateur
    """
    global df, fenT, cb1, cb2, scaleMin, scaleMax, text1, label_mess, cb_Liste

    # Calcul du dataFrame
    arr_ = cb1.get()
    esp_ = cb2.get()
    min_ = scaleMin.get()
    max_ = scaleMax.get()

    df1 = df[(df["HAUTEUR_m"] >= min_) & (df["HAUTEUR_m"] <= max_)]
    if arr_ != "TOUT":
        df2 = df1[df1['ARRONDISSEMENT'].str.contains(arr_, na=False)]
    else:
        df2 = df1
    if esp_ != "TOUT":
        dft = df2[df2['LIBELLEFRANCAIS'].str.contains(esp_, na=False)]
    else:
        dft = df2

    if not gmap: # Cache les colonnes demandées sauf pour gmap
        # Liste les colonnes choisies à afficher
        list_Aff = []
        for e in cb_Liste:
            if e[0].get():
                list_Aff.append(e[1].cget("text"))

        # MAJ du dataframe
        dft = dft[list_Aff]

    # Update Message
    label_mess.config(text = "{:,}".format(dft.shape[0]) + " enregistrements trouvés")
    fenT.title('Par Choix (' + "{:,}".format(dft.shape[0]) + " enregistrements trouvés)")    # Modification du titre de la fenetre Windows

    return dft

def export_csv():

    global df, cb1, cb2, fenT

    dft = retourne_DF_filtre()

    file = g.filesavebox(default="D:\BIGDATA\*.csv", filetypes="*.csv,*.txt")

    try:
        dft.to_csv(file,index = None, header=True, sep=';') # sauve le nouveau fichier en csv
        mess = "Sauvegarde effectuée dans le fichier:\n" + file
        messagebox.showinfo("Exportation", mess)
    except:
        mess = "Erreur lors de l'exportation du fichier \n" + file
        messagebox.showinfo("Exportation", mess)

    fenT.focus_set()

    return None

def dessine():
    """
        Affiche un DataFrame suivant les paramètres suivant
        Arrondissement, Valeur Min, Valeur Max
    """

    global df, fenT, cb1, cb2, scaleMin, scaleMax, text1, label_mess, cb_Liste

    # Fonction qui filtre la DF
    dft = retourne_DF_filtre()

    """
    # Liste les colonnes choisies à afficher
    list_Aff = []
    for e in cb_Liste:
        if e[0].get():
            list_Aff.append(e[1].cget("text"))

    # MAJ du dataframe
    dft = dft[list_Aff]
    """

    # Affiche le textedf1
    text1.delete(1.0, END) # Supprime le contenu
    text1.insert(END, tabulate(dft, headers="keys", showindex=False, tablefmt="github")) #, headers=['HAUTEUR', 'QTE'], tablefmt='fancy_grid')) headers=list_Aff,

    return None

def callbackFuncARR(event):
    global cb1, cb2

    #cb2.slistbox.listbox.delete(0, Tix.END)

    # Affiche dans la combobox les especes pour un arrondissement
    # donné.

    arr_ = cb1.get()
    if arr_ != "TOUT":
        df1 = df[df['ARRONDISSEMENT'].str.contains(arr_, na=False)]
    else:
        df1 = df
    df_Esp = df1.groupby("LIBELLEFRANCAIS").size()

    liste = []
    liste.append("TOUT")            # Ajoute 'TOUT' à la liste
    for l in df_Esp.iteritems():
        if len(l[0].strip()) > 0:  # Supprime les espaces et test si len > 0
            liste.append(l[0])
    cb2.config(values=liste) # Ajoute la liste au comboBox
    cb2.set("TOUT")  # Force sur le 1er element (TOUT)

def par_choix():
    """
        Affichage et gestion de la fenetre de filtres
    """
    global df, fen1, cb1, cb2, scaleMin, scaleMax, text1, label_mess, cb_Liste, fenT

    if df.shape[0] > 0:  # Dataframe non vide

        df_Arr = df.groupby("ARRONDISSEMENT").size()
        df_Esp = df.groupby("LIBELLEFRANCAIS").size()
        df_Hauteur_Max = df[df["HAUTEUR_m"]<=40]["HAUTEUR_m"].max()
        df_Hauteur_Min = df["HAUTEUR_m"].min()

        fenT = Toplevel(fen1) #,height=25,width=25
        #print(fenT.winfo_screenmmwidth)
        fenT.geometry("1200x800")
        fenT.title("Par Choix")
        fenT.maxsize(width= 1200, height=800)

        # Création des composants (Widgets) dans la fenetre
        menubar = Menu(fenT)
        menubar.add_command(label="Fermer", command=fenT.destroy)
        # Affiche le menu
        fenT.config(menu=menubar)

        scrollbar = Scrollbar(fenT)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ComboBox
        lab1 = Label(fenT,text="Arrondisement:")
        lab1.place(x = 5, y = 5)
        liste = []
        liste.append("TOUT")            # Ajoute 'TOUT' à la liste
        for l in df_Arr.iteritems():
            if len(l[0].strip()) > 0:  # Supprime les espaces et test si len > 0
                liste.append(l[0])
        cb1 = ttk.Combobox(fenT,values=liste) # Ajoute la liste au comboBox
        cb1.place(x = 100, y = 5)
        cb1.set("TOUT")  # Force sur le 1er element (TOUT)
        cb1.bind("<<ComboboxSelected>>", callbackFuncARR)  # Gere l'evenement selection
        cb1.focus_set() # Focus sur le combBox

        lab3 = Label(fenT,text="Espece:")
        lab3.place(x = 5, y = 30)
        liste = []
        liste.append("TOUT")            # Ajoute 'TOUT' à la liste
        for l in df_Esp.iteritems():
            if len(l[0].strip()) > 0:  # Supprime les espaces et test si len > 0
                liste.append(l[0])
        cb2 = ttk.Combobox(fenT,values=liste) # Ajoute la liste au comboBox
        cb2.place(x = 100, y = 30)
        cb2.set("TOUT")  # Force sur le 1er element (TOUT)

        # Hauteur Min/Max
        hauteur_labelframe = LabelFrame(fenT, text="Hauteur", height=120, width=200)
        hauteur_labelframe.place(x = 280, y = 5)

        lab2 = Label(hauteur_labelframe,text="Min:")
        lab2.place(x = 5, y = 10)
        scaleValMin = DoubleVar()
        scaleMin = Scale( hauteur_labelframe, variable = scaleValMin, from_ = df_Hauteur_Min, to = df_Hauteur_Max, orient = HORIZONTAL)
        scaleMin.set(df_Hauteur_Min)
        scaleMin.place(x = 40, y = 0)

        lab2 = Label(hauteur_labelframe,text="Max:")
        lab2.place(x = 5, y = 55)
        scaleValMax = DoubleVar()
        scaleMax = Scale( hauteur_labelframe, variable = scaleValMax, from_ = df_Hauteur_Min, to = df_Hauteur_Max, orient = HORIZONTAL)
        scaleMax.set(df_Hauteur_Max)
        scaleMax.place(x = 40, y = 45)

        # Nom des colonnes dans des checkboxs
        cb_Liste = []
        idx = 0
        for nomCol in df.columns:
            cbl = []
            cb_ = IntVar()
            cb = Checkbutton(fenT, text = nomCol, variable = cb_)
            cb.select()
            cb.place(x = 500, y = idx*20 + 5)
            cbl.append(cb_)
            cbl.append(cb)
            cb_Liste.append(cbl)
            idx +=1

        # Bouton Filtre
        bouton_Ok = Button(fenT,text = "Filtre",command = dessine, pady=5)
        bouton_Ok.place(x = 50, y = 80)

        # Bouton Carte
        bouton_Carte = Button(fenT,text = "Carte...",command = show_Browser, pady=5)
        bouton_Carte.place(x = 130, y = 80)

        # Bouton Export
        bouton_Carte = Button(fenT,text = "Export...",command = export_csv, pady=5)
        bouton_Carte.place(x = 210, y = 80)

        # Zone text
        text1 = Text(fenT, wrap=WORD, yscrollcommand=scrollbar.set)
        text1.place(x = 1, y = 130)
        text1.config(height=40, width=146)
        scrollbar.config(command=text1.yview)

        # Message
        label_mess = Label(fenT,text="",bg = "lightgray")
        label_mess.place(x = 1, y = 800-23)
        label_mess.config(height = 1, width = 167) #798

        fenT.mainloop()
    else:
        mess = "Aucune donnée à afficher."
        messagebox.showinfo("Erreur", mess)

    return None

def show_Browser():
    """
        Affiche une carte GMAP dans un browser suivant
        les paramètres suivant Arrondissement, Valeur Min, Valeur Max et Espèce
    """

    global df, cb1, scaleMin, scaleMax, text1, label_mess, cb_Liste, fenT

    arr_ = cb1.get()
    dft = retourne_DF_filtre(gmap=True)

    locations = []
    for index, row in dft.iterrows():
        long,lat = row["geo_point_2d"].split(",")
        locations.append((float(long),float(lat)))

    # Place map
    # First two arugments are the geogrphical coordinates .i.e. Latitude and Longitude
    # and the zoom resolution.
    gmap = gmplot.GoogleMapPlotter(48.858478, 2.342539, 12)   # Centre de Paris
    gmap.apikey = "AIzaSyB-ERbM70w9Q-hhEtOKq7I1JD-g9XJ3n9M"

    # Scatter points
    top_attraction_lats, top_attraction_lons = zip(*locations)
    #gmap.scatter(top_attraction_lats, top_attraction_lons, '#00FF00', size=5, marker=False)
    gmap.heatmap(top_attraction_lats, top_attraction_lons)
    gmap.scatter(top_attraction_lats, top_attraction_lons, '#00FF00', marker=True)

    # Marker
    hidden_gem_lat, hidden_gem_lon = 48.858478, 2.342539
    gmap.marker(hidden_gem_lat, hidden_gem_lon, '#FF0000')

    # Location where you want to save your file.
    date = datetime.datetime.now()
    file_name = ("{}-{}-{}_{}-{}-{}_{}".format(date.year,date.month,date.day,date.hour,date.minute,date.second,arr_))
    html_file = "D:\\Data\\www\\" + file_name + ".html"
    gmap.draw(html_file)
    webbrowser.open(html_file)          # Affiche dans un browser

    return None

def show_fenetre_text(dft,titre="DB Arbres",fichier=None):
    """
        Affiche une fenetre montrant le resultat d'une dataframe.
        'fichier' est le path+nom d'une image à afficher en plus du texte
    """

    global fen1

    if dft.shape[0] > 0:  # Dataframe non vide
        fenT = Toplevel(fen1) #,height=25,width=25
        fenT.geometry("1024x800")
        fenT.title(titre)
        fenT.maxsize(width= 1024, height=800)

        # Création des composants (Widgets) dans la fenetre
        menubar = Menu(fenT)
        menubar.add_command(label="Fermer", command=fenT.destroy)
        # Affiche le menu
        fenT.config(menu=menubar)

        scrollbar = Scrollbar(fenT)
        scrollbar.pack(side=RIGHT, fill=Y)

        text1 = Text(fenT, wrap=WORD, yscrollcommand=scrollbar.set)
        text1.place(x = 0, y = 0)
        h = fenT.winfo_height()
        w = fenT.winfo_width()

        text1.config(height=50, width=125)
        scrollbar.config(command=text1.yview)

        # Affichage d'une image si passée en paramètre
        if fichier != None:
            ## Ouverture du fichier
            image = Image.open(fichier)
            ## Remplace PhotoImage de Tkinter par celui de PIL
            photo = ImageTk.PhotoImage(image)
            text1.image_create(END, image=photo)
            text1.insert(END,'\n')

        # Affiche le texte
        text1.insert(END, tabulate(dft, headers=dft, showindex=False , tablefmt='fancy_grid'))

        fenT.focus_set()    # Donne le focus à la fenetre
        fenT.mainloop()
    else:
        mess = "Aucune donnée à afficher."
        messagebox.showinfo("Erreur", mess)
    return None

def total_Arbre_par_Arrondissement():
    """
        Récupère le Nb d'arbre par Arrondissement
    """

    # Nombre d'arbres par arrondissement en tableau texte
    print("Total arbres sur le territoire parisien et les cimetières extra-muros entre 1 et 40m")
    df1 = df[(df["HAUTEUR_m"] >= 1) & (df["HAUTEUR_m"] <= 40)]   # Ne recupere que les arbres entre 1 m et 40 m
    df1 = df1.groupby(["ARRONDISSEMENT"]).size().reset_index(name='NOMBRE')

    show_fenetre_text(df1,"Total arbres sur le territoire parisien et les cimetières extra-muros entre 1 et 40m") # Affiche le texte dans une autre fenetre

    return None

def sauve_Graphe(fichier):
    # Sauve le graphe
    if os.path.isfile(fichier):
        os.remove(fichier)
    plt.savefig(fichier,orientation = 'landscape')

def hauteur_Min_Max_par_ARRONDISSEMENT():

    # Hauteur Min/Max par ARRONDISSEMENT
    # ----------------------------------

    # Définit la taille des graphiques
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]

    # Set figure width and height
    fig_size[0] = 10
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size

    df1 = df[(df["HAUTEUR_m"] >= 1) & (df["HAUTEUR_m"] <= 40)]   # Ne recupere que les arbres entre 1 m et 40 m
    df1 = df1[df1['ARRONDISSEMENT'].str.contains("PARIS")]       # Ne recupere que les Arrondissement de PARIS

    dfmin = df1.groupby(["ARRONDISSEMENT"])["HAUTEUR_m"].min()   # Création d'une liste avec la taille min par Arrondissement
    dfmax = df1.groupby(["ARRONDISSEMENT"])["HAUTEUR_m"].max()   # Création d'une liste avec la taille max par Arrondissement

    df2 = pd.concat([dfmin, dfmax], axis=1).reset_index()    # Création d'une dataframe avec les deux listes
    df2 = df2.set_axis(['ARRONDISSEMENT','MIN', 'MAX'], axis=1, inplace=False)  # Nommage des colonnes

    # Boucle sur les elements, puis dessine manuellement les barres en les décalant
    for index, row in df2.iterrows():
        plt.bar(row["ARRONDISSEMENT"].replace(" ARRDT", "") , 0, color = 'b', width = 0.25) # + 0.00
        plt_min = plt.bar(index-0.45/2 , row["MIN"], color = 'b', width = 0.45) # + 0.00
        plt_max = plt.bar(index+0.45/2 , row["MAX"], color = 'g', width = 0.45) # + 0.25

    plt.title('Hauteur Min/Max des arbres par Arrondissement')    # Titre
    plt.ylabel("Hauteur (m)")
    plt.xticks(rotation=50)
    plt.grid(True)                             # Affichage d'une grille
    plt.legend((plt_min,plt_max),('MIN', 'MAX'),loc='upper right')  # Ajoute une légende
    #plt.show()

    # Sauve le graphe
    fichier = 'hauteur_Min_Max_par_ARRONDISSEMENT.png'
    sauve_Graphe(fichier)

    # Clear the current axes.
    plt.cla()
    # Clear the current figure.
    plt.clf()
    # Closes all the figure windows.
    plt.close('all')

    show_fenetre_text(df2,"Hauteur Min/Max par ARRONDISSEMENT",fichier) # Affiche le texte dans une autre fenetre

    return None

def hauteur_Min_Max_par_DOMANIALITE():

    # Hauteur Min/Max par DOMANIALITE
    # -------------------------------

    # Définit la taille des graphiques
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]

    # Set figure width to 15 and height to 10
    fig_size[0] = 10
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size

    df1 = df[(df["HAUTEUR_m"] >= 1) & (df["HAUTEUR_m"] <= 40)]   # Ne recupere que les arbres entre 1 m et 40 m

    dfmin = df1.groupby(["DOMANIALITE"])["HAUTEUR_m"].min()   # Création d'une liste avec la taille min par Arrondissement
    dfmax = df1.groupby(["DOMANIALITE"])["HAUTEUR_m"].max()   # Création d'une liste avec la taille max par Arrondissement

    df2 = pd.concat([dfmin, dfmax], axis=1).reset_index()    # Création d'une dataframe avec les deux listes
    df2 = df2.set_axis(['DOMANIALITE','MIN', 'MAX'], axis=1, inplace=False)  # Nommage des colonnes

    ax = plt.gca() # gca stands for 'get current axis'
    df2.plot(kind='bar',x='DOMANIALITE',y='MAX', color='blue', ax=ax)  # Création des 2 graphes
    df2.plot(kind='bar',x='DOMANIALITE',y='MIN', color='red', ax=ax)

    plt.title('Min/Max par DOMANIALITE')    # Titre
    plt.ylabel("Hauteur (m)")
    plt.xticks(rotation=0)
    plt.grid(True)                             # Affichage d'une grille

    # Sauve le graphe
    fichier = 'hauteur_Min_Max_par_DOMANIALITE.png'
    sauve_Graphe(fichier)

    # Clear the current axes.
    plt.cla()
    # Clear the current figure.
    plt.clf()
    # Closes all the figure windows.
    plt.close('all')

    show_fenetre_text(df2,"Hauteur Min/Max par DOMANIALITE",fichier) # Affiche les données dans une autre fenetre

    return None

def affichage_taille_arbre():
    # Affiche la quantité d'arbres dont la hauteur est inférieure ou egale à 40

    global df

    df1 = df.groupby(["HAUTEUR_m"]).size().reset_index(name='NOMBRE')   # Recupère la qte par hauteur
    df2 = df1[(df1["HAUTEUR_m"] <= 40)]   # Filtre sur la hauteur <= 40
    df2 = df2.set_axis(['HAUTEUR', 'QTE'], axis=1, inplace=False)  # Nommage des colonnes
    #df2 = df2.head(200)

    df2.plot(kind='bar',x='HAUTEUR',y='QTE',color='blue')
    plt.title('Total arbres < à 40m sur territoire parisien et cimetières extra-muros')    # Titre
    plt.ylabel("Qte")
    plt.xlabel("Hauteur en mètre")

        # Sauve le graphe
    fichier = 'hauteur_arbre.png'
    sauve_Graphe(fichier)

    # Clear the current axes.
    plt.cla()
    # Clear the current figure.
    plt.clf()
    # Closes all the figure windows.
    plt.close('all')

    show_fenetre_text(df2,"Quantité d'arbres dont la hauteur est inférieure ou egale à 40",fichier)

    return None

def importDB_URL():
    # Définir les variables globales
    global df, menubar, message

    message.config(text="Importation en cours. Veuillez patienter...")
    message.update()

    #affichage de l'URL
    url='https://opendata.paris.fr/explore/dataset/les-arbres/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true'
    #chargement du fichier
    df = pd.read_csv(url,
        usecols = ['IDBASE','ARRONDISSEMENT','DOMANIALITE','LIBELLEFRANCAIS','HAUTEUR (m)','geo_point_2d'],
        dtype = {'IDBASE': int,'HAUTEUR (m)': int},
        sep=';')
    #change le nom de l'entete afin de supprimer les caracteres non autorisés
    df.rename(columns={'HAUTEUR (m)': 'HAUTEUR_m'}, inplace=True)

    df.to_csv(r'D:\BIGDATA\Datas_arbres.csv',index = None, header=True, sep=';') # sauve le nouveau fichier en csv

    mess = "Téléchargement effectué.\n" + "{:,}".format(df.shape[0]) + " enregistrements récupérés. Sauvegarde sur le PC effectuée"
    messagebox.showinfo("Importation", mess)

    # Active le menu graphe
    menubar.entryconfig("Graph", state="normal")

    message.config(text='D:\BIGDATA\Datas_arbres.csv' + " --> " + "{:,}".format(df.shape[0]) + " enregistrements")

def importDB_CSV():
    global df, menubar, message

    file = g.fileopenbox(default="D:\BIGDATA\*.*")

    df = pd.read_csv(file,
        #usecols = ['IDBASE','ARRONDISSEMENT','DOMANIALITE','LIBELLEFRANCAIS','HAUTEUR (m)','geo_point_2d'],
        usecols = ['IDBASE','ARRONDISSEMENT','DOMANIALITE','LIBELLEFRANCAIS','HAUTEUR_m','geo_point_2d'],
        dtype = {'IDBASE': int,'HAUTEUR (m)': int},
        sep=';')
    #change le nom de l'entete afin de supprimer les caracteres non autorisés
    #df.rename(columns={'HAUTEUR (m)': 'HAUTEUR_m'}, inplace=True)

    mess = "Téléchargement effectué.\n" + "{:,}".format(df.shape[0]) + " enregistrements récupérés."
    messagebox.showinfo("Importation", mess)

    # Active le menu graphe
    menubar.entryconfig("Graph", state="normal")

    message.config(text=file + " --> " + "{:,}".format(df.shape[0]) + " enregistrements")

    return None

def main():
    # Définir les variables globales
    global df
    global fen1
    global menubar, message

    # Parametrage de Pandas et de MatPlotLib

    pd.set_option('display.max_columns', 50)    # Force pandas à afficher plus de 8 colonnes
    pd.set_option('display.max_rows', 1000)     # Force à afficher plus de 80 ligne
    pd.set_option('display.width', 1000)        # Force à afficher les longues chaines

    # Programme principal
    fen1 = Tk()                     # Création de l'instance de la fentetre
    fen1.title('DB Arbres')    # Modification du titre de la fenetre Windows
    fen1.geometry("400x250")
    fen1.maxsize(width= 400, height=250)

    # Création des composants (Widgets) dans la fenetre
    menubar = Menu(fen1)
    #•menubar.add_command(label="Importer DB", command=importDB)

    graph = Menu(menubar, tearoff=0)
    graph.add_command(label="WEB", command=importDB_URL)
    graph.add_separator()
    graph.add_command(label="CSV...", command=importDB_CSV)
    menubar.add_cascade(label="Import Data", menu=graph)

    graph = Menu(menubar, tearoff=0)
    graph.add_command(label="Total arbre par Hauter", command=affichage_taille_arbre)
    graph.add_command(label="Total arbre par Arrondissement", command=total_Arbre_par_Arrondissement)
    graph.add_command(label="Hauteur Min/Max par DOMANIALITE", command=hauteur_Min_Max_par_DOMANIALITE)
    graph.add_command(label="Hauteur Min/Max par ARRONDISSEMENT", command=hauteur_Min_Max_par_ARRONDISSEMENT)
    graph.add_separator()
    graph.add_command(label="Liste Parametrable...", command=par_choix)
    #graph.add_command(label="Cartes ...", command=show_Browser)
    menubar.add_cascade(label="Graph", menu=graph)
    #self.menubar.entryconfig("Test2", state="normal")
    menubar.entryconfig("Graph", state="disabled")   # Déactivé par défaut

    menubar.add_command(label="Quitter", command=fen1.destroy)

    # Affiche le menu
    fen1.config(menu=menubar)

    # Création de la frame du bas
    message = Label(fen1,text="GRETA 2019", bg = 'lightgray')
    message.place(x = 1, y = 228)
    message.config(height=1, width=56)

    # Image de fond
    c = Canvas(fen1, bg = 'white' )
    c.place(x=0,y=0)
    h = 225
    w = 400
    c.config(height=h, width=w)
    img = Image.open("arbre.jpg")

    img = img.resize((w, h), Image.ANTIALIAS)
    img_fond = ImageTk.PhotoImage(img)
    #c.create_image(h/2,w/2,image=img_fond)
    c.create_image(w/2,h/2,image=img_fond)

    fen1.mainloop()         # Boucle sur les événements

if __name__ == '__main__':
    main()
