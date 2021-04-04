from fonctions_scrap import getlivre
# Télécharge données livres de l'url
# Ouvre un répertoire pour stockage
# Télécharge image de couverture dans répertoire
# Ecrit données dans csv stocké dans répertoire

url = input("URL de votre livre : ")
getlivre(url)
