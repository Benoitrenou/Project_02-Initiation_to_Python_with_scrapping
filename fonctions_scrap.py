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
    """
    Requête pour récupérer données HTML de la page
    Renvoie analyse via soup base librairie 'lxml'
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def extractcateg(url):
    """
    Extrait toutes les catégories disponibles du site
    Renvoie les catégories dans liste categories_urls
    """
    soup = getresponseandsoup(url)
    categories_urls = [
        x.get("href")
        for x in soup.find_all("a", href=re.compile("catalogue/category/books"))
    ]
    categories_urls = categories_urls[1:]
    return categories_urls


def geturlscateg(url, categorie_choisie):
    """
    Modifie url source de la catégorie en fonction du nombre de pages
    Renvoie urls modifiées dans listes urls
    """
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
    """
    Extrait les urls de tous les articles de la catégorie analysée
    Renvoie ces urls dans liste liens_articles
    """
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
    """
    Extrait données requises de l'article
    Stock ces données dans liste data
    soup.find utilise BS pour trouver balises correspondantes dans code HTML et extraire donnée souhaitée
    """
    soup = getresponseandsoup(url)
    title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text
    title= title.decode('utf-8').encode('latin1')
    print (title)
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
    data = [title, UPC, prixHT, prixTTC, stock, CATEG, DESC, note, image_url, url]
    print(f"Données livre {title} stockées pour écriture")
    return data


def createdirectory(titre):
    """
    Crée un répertoire nommé d'après nom catégorie/livre analysé.e et moment analyse
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    titre = f"{titre:.60}"
    titre_file = sanitize_filepath(titre)
    path = f"{os.getcwd()}/fichiers-{titre_file}-{date}"
    os.mkdir(path)
    cwd = os.getcwd()
    print("Dossier d'enregistrement des fichiers :", path, "\n")
    return path


def downldimg(titre, categorie, image_url, path):
    """
    Télécharge image du livre analysé
    Limite nombre de caractères pour titre de l'image pour éviter erreur
    Message d'erreur prévu si image non téléchargée
    """
    titre_image = sanitize_filename(titre)
    img_name = f"Image_{titre_image:.60}_{categorie}.jpeg"
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(f"{path}/{img_name}", "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(f"Image {titre_image} téléchargée")
    else:
        print(f"Image {titre_image} non téléchargée - problème laison URL")


def writecsv(name, listes, path):
    """
    Ouvre et écrit dans un fichier csv données en argument listes dans répertoire path
    """
    if listes is None or len(listes) == 0:
        print("Erreur : données vides")
        return
    titre_csv = sanitize_filename(name)
    filename = f"Data-{titre_csv:.60}.csv"
    with open(f"{path}/{filename}", "w", encoding="utf-8", newline="") as file:
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


def getlivre(url, workingdirectory):
    """
    Récupère données sans écriture d'un livre
    Télécharge l'image du livre
    Renvoie données du livre
    """
    data = getbookdata(url)
    downldimg(
        titre=data[0], categorie=data[5], image_url=data[8], path=f"{workingdirectory}"
    )
    return data


def getcategorie(categorie_choisie):
    """
    Rassemble fonctions utiles au scrapping d'une catégorie entière du site, choisie ou non
    """
    url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur : nom de la catégorie introuvable")
        return -1
    urls_categ = geturlscateg(url, categorie_choisie)
    liens_articles = getarticleslinks(urls_categ)
    workingdirectory = createdirectory(titre=categorie_choisie)
    books = []
    for url in liens_articles:
        data = getlivre(url=url, workingdirectory=workingdirectory)
        books.append(data)
    writecsv(name=categorie_choisie, listes=books, path=workingdirectory)


def scrapcategorie(choix):
    """
    Definit scrapping catégorie unique ou toutes les catégories selon script choisi
    """
    categories_urls = extractcateg("http://books.toscrape.com/index.html")
    if choix is True:
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


def scraplivre(url):
    """
    Rassemble les fonctions nécessaires au scrapping d'un seul livre
    Récupère données - Crée répertoire - Télécharge image - Ouvre et écrit csv
    """
    data = getbookdata(url)
    workingdirectory = createdirectory(titre=data[0])
    downldimg(
        titre=data[0], categorie=data[5], image_url=data[8], path=workingdirectory
    )
    writecsv(name=data[0], listes=[data], path=workingdirectory)
