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


def main():
    #import du fichier les-arbres.csv avec selection des colonnes utilisable pour l’analyse du client
    df = pd.read_csv("D:\BIGDATA\Datas_arbres.csv", sep=';')

    print(df.columns)

    print("Nombre d'arbre par ARRONDISSEMENT/NOM ARBRE")
    print(df.groupby(["ARRONDISSEMENT","LIBELLEFRANCAIS"]).size().reset_index(name='NOMBRE'))

    print("Nombre d'arbre par ARRONDISSEMENT")
    print(df.groupby(["ARRONDISSEMENT"]).size().reset_index(name='NOMBRE'))






if __name__ == '__main__':
    main()
