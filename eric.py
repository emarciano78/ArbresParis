#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eric
#
# Created:     13/06/2019
# Copyright:   (c) eric 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import pandas as pd

import pyperclip        # Permet de copier dans le clipboard


def main():


    pd.set_option('display.max_columns', 50)    # Force pandas à afficher plus de 8 colonnes
    pd.set_option('display.width', 1000)        # Force à afficher plus de 80 colonnes

    #import du fichier les-arbres.csv avec selection des colonnes utilisable pour l’analyse du client
    df = pd.read_csv("D:\BIGDATA\Datas_arbres.csv", sep=';')

    print(df.head())

    print(df.columns)

    print("Nombre d'arbre par ARRONDISSEMENT/NOM ARBRE")
    df1 = df.groupby(["ARRONDISSEMENT","LIBELLEFRANCAIS"]).size().reset_index(name='NOMBRE')
    print(df1)

    print("Nombre d'arbre par ARRONDISSEMENT")
    df2 = df.groupby(["ARRONDISSEMENT"]).size().reset_index(name='NOMBRE')
    print(df2)


    print(df.describe().T)




if __name__ == '__main__':
    main()
