# -*- coding: utf-8 -*-
import re
import csv
import shutil
import os
from math import ceil
import datetime
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathvalidate import sanitize_filepath
import requests


def getresponseandsoup(url):
    # Requête pour récupérer données HTML de la page - analyse via soup base librairie 'lxml'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def extractcateg(url):
	# Extrait toutes les catégories disponibles du site
	# Stock les catégories dans liste categories_urls
    soup = getresponseandsoup(url)
    categories_urls = [
        x.get("href")
        for x in soup.find_all("a", href=re.compile("catalogue/category/books"))
    ]
    categories_urls = categories_urls[1:]
    return categories_urls


def geturlscateg(url, categorie_choisie):
	# Modifie url source de la catégorie en fonction du nombre de pages
	# Stock urls modifiées dans listes urls
    soup = getresponseandsoup(url)
    results = soup.find("form", {"class": "form-horizontal"}).find("strong").text
    nombre_pages = ceil(float(results) / 20)
    urls = []
    if nombre_pages != 1:
        for i in range(1, nombre_pages + 1):
            url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/page-{str(i)}.html"
            urls.append(url)
    else:
        urls.append(url)
    return urls


def getarticleslinks(urls):
	# Extrait les urls de tous les articles de la catégorie analysée
	# Stock ces urls dans liste liens_articles
    liens_articles = []
    for j in urls:
        soup = getresponseandsoup(j)
        articles = soup.findAll("article")
        for article in articles:
            a = article.find("a")
            link = a["href"].replace("../../../", "")
            liens_articles.append(f"http://books.toscrape.com/catalogue/{link}")
    print(f"\nNombre de livres de cette catégorie : {len(liens_articles)}\n")
    return liens_articles


def getbookdata(url):
	# Extrait données requises de l'article
	# Stock ces données dans liste data
    soup = getresponseandsoup(url)
    # soup.find utilise BS pour trouver balises correspondantes dans code HTML et extraire donnée souhaitée
    title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text
    upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
    UPC = upc[0].text
    prixHT = upc[2].text.replace("Â", "").replace("£", "")
    prixTTC = upc[3].text.replace("Â", "").replace("£", "")
    stock = re.sub("[^0-9]", "", soup.find("p", class_="instock availability").text)
    categorie = soup.find("ul", {"class": "breadcrumb"}).find_all("li")
    CATEG = categorie[2].text.replace("\n", "")
    description = soup.find("article", {"class": "product_page"}).find_all("p")
    DESC = description[3].text.replace(";", ",")
    image = soup.find("img")
    image_url = f'http://books.toscrape.com/{image["src"]}'
    rating = soup.find("p", class_=re.compile("star-rating")).get("class")[1]
    rating_dic = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    note = rating_dic[rating]
    data = [title, UPC, prixHT, prixTTC, stock, CATEG, DESC.encode( 'ascii', errors='ignore' ), note, image_url, url]
    print(f"Données livre {title} stockées pour écriture")
    return data


def createdirectory(titre):
	# Ouvre un répertoire nommé d'après nom catégorie/livre analysé.e et moment analyse
	# Ouvre ce répertoire comme répertoire de travail
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    titre_file = sanitize_filepath(titre)
    path = f"{os.getcwd()}/fichiers-{titre_file}-{date}"
    os.mkdir(path)
    os.chdir(path)
    cwd = os.getcwd()
    print("Dossier d'enregistrement des fichiers :", cwd, "\n")


def downldimg(titre, categorie, image_url):
	# Télécharge image du livre analysé
    titre_image = sanitize_filename(titre)
    img_name = f"Image_{titre_image:.60}_{categorie}.jpeg"
    # Limite nombre de caractères pour titre de l'image pour éviter erreur
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(img_name, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(f"Image {titre_image} téléchargée")
    else:
        print(f"Image {titre_image} non téléchargée - problème laison URL")
    # message d'erreur prévu


def writecsv(name, listes):
	# Ouvre et écrit dans un fichier csv données du livre analysé issues de fonction getbookdata
    if listes is None or len(listes) == 0:
        print("Erreur : données vides")
        return
    filename = f"Data-{name}.csv"
    with open(f"{filename}", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=";")
        entête = [
            "Titre",
            "UPC",
            "Prix HT",
            "Prix TTC",
            "Stock",
            "Catégorie",
            "Description",
            "Note sur 5",
            "URL image",
            "URL livre",
        ]
        writer.writerow(entête)
        writer.writerows(listes)
        print(
            f"\nDonnées de {name} téléchargées et disponibles sur fichier Data-{name}.csv\n"
        )


def getlivre(url, categorie=None):
	# Rassemble fonctions utiles au scrapping d'un livre sur base de son url
    data = getbookdata(url)
    if categorie is None:
        createdirectory(data[0])
    downldimg(titre=data[0], categorie=data[5], image_url=data[8])
    books = []
    books.append(data)
    if categorie is None:
        writecsv(name=data[0], listes=books)
        # Prévoit repousser écriture csv en cas de scrapping global d'une catégorie


def getcategorie(categorie_choisie):
	# Rassemble fonctions utiles au scrapping d'une catégorie entière du site, choisie ou non
    url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur : nom de la catégorie introuvable")
        return -1
    urls_categ = geturlscateg(url, categorie_choisie)
    liens_articles = getarticleslinks(urls_categ)
    createdirectory(titre=categorie_choisie)
    books = []
    for url in liens_articles:
        data = getlivre(url, categorie=categorie_choisie)
        books.append(data)
    writecsv(name=categorie_choisie, listes=books)


def choixcategorie(choix):
	# Definit scrapping catégorie unique ou toutes les catégories selon script choisi
    categories_urls = extractcateg("http://books.toscrape.com/index.html")
    if choix is not None:
        for y in categories_urls:
            print(f'Catégorie disponible : {y.split("/")[3]}')
        categorie_choisie = input(
            "Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?"
        )
        getcategorie(categorie_choisie=categorie_choisie)

    else:
        for j in categories_urls:
            i = j.split("/")[3]
            print(f"Initiation scrapping catégorie {i}\n")
            getcategorie(categorie_choisie=i)
            os.chdir("..")
