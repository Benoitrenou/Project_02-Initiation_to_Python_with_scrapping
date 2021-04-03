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
    soup = getresponseandsoup(url)
    categories_urls = [
        x.get("href")
        for x in soup.find_all("a", href=re.compile("catalogue/category/books"))
    ]
    categories_urls = categories_urls[1:]
    return categories_urls


def geturlscateg(url, categorie_choisie):
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
    soup = getresponseandsoup(url)
    # BeautifulSoup renvoie en réponse code HTML format text en utilisant parser souhaité - 'lxml'
    # soup.find utilise BS pour trouver balises correspondantes dans code HTML et extraire donnée souhaitée
    title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text
    upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
    UPC = upc[0].text
    prixHT = upc[2].text.replace("Â", "").replace("£", "")
    prixTTC = upc[3].text.replace("Â", "").replace("£", "")
    stock = re.sub("[^0-9]", "", soup.find("p", class_="instock availability").text)
    catégorie = soup.find("ul", {"class": "breadcrumb"}).find_all("li")
    CATEG = catégorie[2].text.replace("\n", "")
    description = soup.find("article", {"class": "product_page"}).find_all("p")
    DESC = description[3].text.replace(";", ",")
    image = soup.find("img")
    image_url = f'http://books.toscrape.com/{image["src"]}'
    rating = soup.find("p", class_=re.compile("star-rating")).get("class")[1]
    rating_dic = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    note = rating_dic[rating]
    data = [title, UPC, prixHT, prixTTC, stock, CATEG, DESC, note, image_url, url]
    print(f"\nDonnées livre {title} stockées pour écriture\n")
    return data


def openfile(titre):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    titre_file = sanitize_filepath(titre)
    path = f"{os.getcwd()}/fichiers-{titre_file}-{date}"
    os.mkdir(path)
    os.chdir(path)
    cwd = os.getcwd()
    print("Dossier d'enregistrement des fichiers :", cwd)


def downldimg(titre, categorie, image_url):
    titre_image = sanitize_filename(titre)
    img_name = f"Image_{titre_image:.60}_{categorie}.jpeg"
    # Limite nombre de caractères pour titre de l'image pour éviter erreur
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(img_name, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(f" Image {titre_image} téléchargée\n")
    else:
        print(f"Image {titre_image} non téléchargée - problème laison URL\n")
    # message d'erreur prévu

def opencsv(name, liste, listes):
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
        if liste != None:
            writer.writerow(liste)
        if listes != None:
            writer.writerows(listes)
    print(f"Données de {name} téléchargées et disponibles sur fichier Data-{name}.csv")
