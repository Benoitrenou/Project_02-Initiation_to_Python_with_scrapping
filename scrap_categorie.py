import requests
from fonctions_scrap import extractcateg
from fonctions_scrap import geturlscateg
from fonctions_scrap import getarticleslinks
from fonctions_scrap import getbookdata
from fonctions_scrap import openfile
from fonctions_scrap import downldimg
from fonctions_scrap import opencsv

categories_urls = extractcateg("http://books.toscrape.com/index.html")
# Print toutes les catégories pour permettre à utilisateur de choisir
for y in categories_urls:
    print(f'Catégorie disponible : {y.split("/")[3]}\n')


# Choix catégorie par utilisateur et modif URL en conséquence
categorie_choisie = input(
    "Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?"
)
url = (
    f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
)
response = requests.get(url)
while response.status_code != 200:
    print("Erreur - vérifiez la catégorie que vous avez entrée ou votre connexion\n")
    categorie_choisie = input(
        "Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?"
    )
    url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
    response = requests.get(url)
# Boucle while vérifie catégorie entrée correct via requête

urls_categ = geturlscateg(url, categorie_choisie)
# Liste urls_categ stock les urls des pages de la catégorie

liens_articles = getarticleslinks(urls_categ)
# Liste liens_articles stock les urls de chaque article

books = []
for url in liens_articles:
    data_article = getbookdata(url)
    books.append(data_article)
# liste books de listes datas qui contiennent infos de chaque livre
openfile(titre=categorie_choisie)
for data_article in books:
    downldimg(
        titre=data_article[0],
        categorie=data_article[5],
        image_url=data_article[8]
    )
opencsv(listes=books, name=categorie_choisie, liste=None)
