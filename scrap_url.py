from fonctions_scrap import getbookdataandimage
#Récupère et stock data - télécharge image
from fonctions_scrap import opencsv
#Ouvre csv pour écriture données

url = input("URL de votre livre : ")
data = getbookdataandimage(url)
opencsv (liste=data, name=data[0], listes=None)