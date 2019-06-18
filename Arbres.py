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

    df1 = df[(df["HAUTEUR_m"] >= 1) & (df["HAUTEUR_m"] <= 10000)]

    df1 = df1.sort_values("LIBELLEFRANCAIS", ascending=True)

    print(df1[:])

    print(df1.shape)

    del df1 # Remove variable


    pass

if __name__ == '__main__':
    main()
