import requests
from datetime import date
import csv
from fonctions_scrap import getresponseandsoup 
from fonctions_scrap import getbookdataandimage
#fonction envoie requête - récupère et parse données HTML - retrouve datas dans code HTML - télécharge image
from fonctions_scrap import extractcateg 
#fonction récupère ensemble des catégories disponibles du site 
from fonctions_scrap import	geturlscateg
#ajuste URL de la catégorie choisie par user dépendamment nmbre articles de la catégorie
from fonctions_scrap import getarticleslinks
#recense tous articles de la catégorie


#Extraction urls des catégories dans une liste categories_urls
categories_urls = extractcateg ("http://books.toscrape.com/index.html")

for j in categories_urls : 
	i = j.split('/')[3]
	print (f'Initiation scrapping catégorie {i}\n')
	url = f"http://books.toscrape.com/catalogue/category/books/{i}/index.html"
	response = requests.get(url)
	#Définition nombre de résultats/pages et modification url en conséquence
	urls_categ = geturlscateg (url, i)
	#Liste urls_categ stock les urls des pages de la catégorie

	# Recenser articles par catégorie
	liens_articles = getarticleslinks (urls_categ) 
	# Liste liens_articles stock les urls de chaque article

	books = [] 
	for url in liens_articles : 
		data_article = getbookdataandimage (url) 
		books.append(data_article)
	#liste books de listes datas qui contiennent infos de chaque livre

	with open(f'Données-{i}-{str(date.today())}.csv', 'w', encoding="utf-8", newline='') as file:
	    writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=';')
	    entête = ["Titre", "UPC", "Prix HT", "Prix TTC", "Stock", "Catégorie", "Description", "Note sur 5", "URL image", "URL livre"]
	    writer.writerow(entête)
	    writer.writerows(books)
	    print (f'\nDonnées {i} téléchargées et disponibles dans fichier Données-{i}-{str(date.today())}.csv\n')
