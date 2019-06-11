#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      eric
#
# Created:     11/06/2019
# Copyright:   (c) eric 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# librairie pandas
import pandas
import csv
import numpy as np


def main():

    #import du fichier les-arbres.csv avec selection des colonnes utilisable pour l’analyse du client
    df = pandas.read_csv("D:\BIGDATA\les-arbres.csv",
        usecols = ['IDBASE','ARRONDISSEMENT','DOMANIALITE','LIBELLEFRANCAIS','HAUTEUR (m)','geo_point_2d'],
        sep=';')
    df.rename(columns={'HAUTEUR (m)': 'HAUTEUR_m'}, inplace=True)
    print('**** sauve le nouveau fichier en csv ****')
    df.to_csv(r'D:\BIGDATA\Datas_arbres.csv',index = None, header=True, sep=';') # sauve le nouveau fichier en csv

if __name__ == '__main__':
    main()
