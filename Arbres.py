#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eric
#
# Created:     15/06/2019
# Copyright:   (c) eric 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas as pd



def main():

    pd.set_option('display.max_columns', 50)    # Force pandas à afficher plus de 8 colonnes
    pd.set_option('display.width', 1000)        # Force à afficher plus de 80 ligne

    df = pd.read_csv("D:\BIGDATA\Datas_arbres.csv", sep=';')

    df1 = df[(df["HAUTEUR_m"] >= 1) & (df["HAUTEUR_m"] <= 40)]
    df2 = df1.groupby(["ARRONDISSEMENT","LIBELLEFRANCAIS"]).size().reset_index(name='NOMBRE')
    df2 = df2.sort_values(["ARRONDISSEMENT","LIBELLEFRANCAIS"])
    df2 = df2.set_axis(['ARRONDISSEMENT','ARBRE', 'QTE'], axis=1, inplace=False)  # Nommage des colonnes

    dfArbre = df1.groupby(["LIBELLEFRANCAIS"]).size().reset_index(name='ARBREBRE') # Liste des arbres

    #print(dfArbre)

    #print(df2.to_string(index=False))

    # Création du dataset principal
    arrs = {}
    arbres = {}

    for index, row in df2.iterrows():
        #print(row["ARRONDISSEMENT"], row["ARBRE"], row["QTE"])
        if row["ARRONDISSEMENT"] not in arrs: # Ajout de l'arrondissement
            arbres = {}
            arbres[row["ARBRE"]] = row["QTE"]
            arrs[row["ARRONDISSEMENT"]] = arbres
        else:
            if row["ARBRE"] not in arrs[row["ARRONDISSEMENT"]]:
                #arbres = arrs[row["ARRONDISSEMENT"]]
                arrs[row["ARRONDISSEMENT"]][row["ARBRE"]] = row["QTE"]
                #arbres[row["ARBRE"]] = row["QTE"]
                #arrs[row["ARRONDISSEMENT"]] = arbres
            else:
                 #arbres =
                 arrs[row["ARRONDISSEMENT"]][row["ARBRE"]] += row["QTE"]
                 #arbres[row["ARBRE"]] += row["QTE"]
                 #arrs[row["ARRONDISSEMENT"]] = arbres
                 a = 1
                 #old_qte + row["QTE"]

    print(arrs)

    dfA = pd.DataFrame(arrs)


    # Nommage des colonnes
    dfA = dfA.set_axis(['BOIS DE BOULOGNE','BOIS DE VINCENNES',
        'HAUTS-DE-SEINE','10E','11E','12E','13E','14E','15E','16E','17E',
        '18E','19E','1ER','20E','2E','3E','4E','5E','6E','7E','8E','9E',
        'SEINE-SAINT-DENIS','VAL-DE-MARNE'], axis=1, inplace=False)


    # Sortie au format csv
    result = dfA.to_csv("output.txt")


if __name__ == '__main__':
    main()
