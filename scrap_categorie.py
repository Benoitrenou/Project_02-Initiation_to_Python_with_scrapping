import requests
import re
from bs4 import BeautifulSoup 
from math import *
from fonctions_scrap import getresponseandsoup 
from fonctions_scrap import getbookdata
from fonctions_scrap import extractcateg 
from fonctions_scrap import	geturlscateg
from fonctions_scrap import getarticleslinks


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
print (urls_categ)
#Liste urls_categ stock les urls des pages de la catégorie

# Recenser articles par catégorie
liens_articles = getarticleslinks (urls_categ) 
print (liens_articles)
# Liste liens_articles stock les urls de chaque article


books = [] 
for url in liens_articles : 
	data_article = getbookdata (url) 
	books.append(data_article)
#liste books de listes datas qui contiennent infos de chaque livre

print (len(books))
print (books)

