import requests
import os
from fonctions_scrap import extractcateg
from fonctions_scrap import geturlscateg
from fonctions_scrap import getarticleslinks
from fonctions_scrap import getbookdata
from fonctions_scrap import openfile
from fonctions_scrap import downldimg
from fonctions_scrap import opencsv

categories_urls = extractcateg("http://books.toscrape.com/index.html")
# Liste categories_urls stock urls de chaque catégorie

for j in categories_urls:
    i = j.split("/")[3]
    print(f"Initiation scrapping catégorie {i}\n")
    url = f"http://books.toscrape.com/catalogue/category/books/{i}/index.html"
    response = requests.get(url)
    urls_categ = geturlscateg(url, i)
    # Liste urls_categ stock les urls des pages de la catégorie
    liens_articles = getarticleslinks(urls_categ)
    # Liste liens_articles stock les urls de chaque article

    books = []
    for url in liens_articles:
        data_article = getbookdata(url)
        books.append(data_article)
    # liste books de listes datas qui contiennent infos de chaque livre
    openfile(titre=i)
    for data_article in books:
        downldimg(
            titre=data_article[0],
            categorie=data_article[5],
            image_url=data_article[8],
        )
    opencsv(listes=books, name=i, liste=None)
    os.chdir('..')
