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

#Print toutes les catégories pour permettre à utilisateur de choisir 
for y in categories_urls:
	print(f'Catégorie disponible : {y.replace("catalogue/category/books/", "").replace("/index.html", "")}')


#Choix catégorie par utilisateur et modif URL en conséquence 
categorie_choisie = input("Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?")
url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
response = requests.get(url)
while response.status_code != 200 : 
	print ('Erreur - vérifiez la catégorie que vous avez entrée ou votre connexion')
	categorie_choisie = input("Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?")
	url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
	response = requests.get(url)
#Boucle while vérifie catgéorie entrée correct via requête 

#Définition nombre de résultats/pages et modification url en conséquence
urls_categ = geturlscateg (url, categorie_choisie)
#Liste urls_categ stock les urls des pages de la catégorie

# Recenser articles par catégorie
liens_articles = getarticleslinks (urls_categ) 
# Liste liens_articles stock les urls de chaque article

books = [] 
for url in liens_articles : 
	data_article = getbookdataandimage (url) 
	books.append(data_article)
#liste books de listes datas qui contiennent infos de chaque livre

with open(f'données{categorie_choisie}-{str(date.today())}.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=';')
    entête = ["Titre", "UPC", "Prix HT", "Prix TTC", "Stock", "Catégorie", "Description", "Note sur 5", "URL image", "URL livre"]
    writer.writerow(entête)
    writer.writerows(books)
