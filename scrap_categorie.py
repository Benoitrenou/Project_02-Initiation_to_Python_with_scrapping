import requests
from fonctions_scrap import getbookdataandimage
#Récupère et stock data - télécharge image
from fonctions_scrap import extractcateg
#Récupère catégories disponibles
from fonctions_scrap import geturlscateg
#Ajuste URL de la catégorie choisie par user fonction nmbre articles de la catégorie
from fonctions_scrap import getarticleslinks
#Recense tous articles de la catégorie
from fonctions_scrap import opencsv
#Ouvre csv pour écriture données

categories_urls = extractcateg("http://books.toscrape.com/index.html")

#Print toutes les catégories pour permettre à utilisateur de choisir
for y in categories_urls:
    print(f'Catégorie disponible : {y.replace("catalogue/category/books/", "").replace("/index.html", "")}\n')


#Choix catégorie par utilisateur et modif URL en conséquence
categorie_choisie = input("Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?")
url = (f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html")
response = requests.get(url)
while response.status_code != 200:
    print("Erreur - vérifiez la catégorie que vous avez entrée ou votre connexion\n")
    categorie_choisie = input("Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?")
    url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
    response = requests.get(url)
#Boucle while vérifie catégorie entrée correct via requête

urls_categ = geturlscateg(url, categorie_choisie)
# Liste urls_categ stock les urls des pages de la catégorie

liens_articles = getarticleslinks(urls_categ)
# Liste liens_articles stock les urls de chaque article

books = []
for url in liens_articles:
    data_article = getbookdataandimage(url)
    books.append(data_article)
# liste books de listes datas qui contiennent infos de chaque livre

opencsv (listes=books, name=categorie_choisie, liste=None)