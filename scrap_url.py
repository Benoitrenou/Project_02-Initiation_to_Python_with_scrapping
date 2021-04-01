import csv
from datetime import date
from fonctions_scrap import getbookdataandimage
#fonction envoie requête - récupère et parse données HTML - retrouve datas dans code HTML - télécharge image

url = input ('URL de votre livre : ')

data = getbookdataandimage (url) 
with open(f'données{data[0]}-{str(date.today())}.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=';')
    entête = ["Titre", "UPC", "Prix HT", "Prix TTC", "Stock", "Catégorie", "Description", "Note sur 5", "URL image", "URL livre"]
    writer.writerow(entête)
    writer.writerow(data)