from fonctions_scrap import getbookdata

# Récupère et stock data - télécharge image
from fonctions_scrap import opencsv

# Ouvre csv pour écriture données
from fonctions_scrap import openfile

# Ouvre dossier pour stocker image et csv
from fonctions_scrap import downldimg

# Télécharge images et stock dans fichier


url = input("URL de votre livre : ")

data = getbookdata(url)
path = openfile(data[0])
downldimg(titre=data[0], categorie=data[5], image_url=data[8], path=path)
opencsv(name=data[0], liste=data, listes=None, path=path)
