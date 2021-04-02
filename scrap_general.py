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
#Liste categories_urls stock urls de chaque catégorie

for j in categories_urls:
    i = j.split("/")[3]
    print(f"Initiation scrapping catégorie {i}\n")
    url = f"http://books.toscrape.com/catalogue/category/books/{i}/index.html"
    response = requests.get(url)
    urls_categ = geturlscateg(url, i)
    #Liste urls_categ stock les urls des pages de la catégorie
    liens_articles = getarticleslinks(urls_categ)
    # Liste liens_articles stock les urls de chaque article

    books = []
    for url in liens_articles:
        data_article = getbookdataandimage(url)
        books.append(data_article)
    # liste books de listes datas qui contiennent infos de chaque livre
    opencsv (listes=books, name=i, liste=None)