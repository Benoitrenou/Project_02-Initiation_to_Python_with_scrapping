import re
import requests
import shutil
from bs4 import BeautifulSoup
from math import *

def getresponseandsoup(url) :
	#Requête pour récupérer données HTML de la page - analyse via soup base librairie 'lxml'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "lxml")
	return soup

def extractcateg (url):
	soup = getresponseandsoup(url)
	categories_urls = [x.get("href") for x in soup.find_all("a", href=re.compile("catalogue/category/books"))]
	categories_urls = categories_urls[1:]
	return categories_urls

def geturlscateg (url, categorie_choisie) : 
	soup = getresponseandsoup(url)
	results = soup.find('form', {'class' : 'form-horizontal'}).find('strong').text
	nombre_pages = ceil(float(results) / 20)
	urls = []
	if nombre_pages != 1 :
		for i in range (1, nombre_pages+1) : 
			url = (f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/page-{str(i)}.html")
			urls.append(url)
	else :
		urls.append (url)
	return urls 

def getarticleslinks (urls) : 
	liens_articles = []
	for j in urls:
	    soup = getresponseandsoup(j)
	    articles = soup.findAll("article")
	    for article in articles:
	        a = article.find("a")
	        link = a["href"].replace("../../../", "")
	        liens_articles.append(f"http://books.toscrape.com/catalogue/{link}")
	print(f"Nombre de livres de cette catégorie : {len(liens_articles)}")
	return liens_articles 

def getbookdataandimage (url) : 
	soup = getresponseandsoup (url)
	#BeautifulSoup renvoie en réponse code HTML format text en utilisant parser souhaité - 'lxml'
	#soup.find utilise BS pour trouver balises correspondantes dans code HTML et extraire donnée souhaitée
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
	data = [title, UPC, prixHT, prixTTC, stock, CATEG, DESC, image_url, note]
	print (f'Données livre {title} téléchargées')

	titre_image = url.replace("http://books.toscrape.com/catalogue/", "").replace("/index.html", "")
	filename = f"Image_{titre_image}_{CATEG}.jpeg"

	r = requests.get(image_url, stream=True)
	if r.status_code == 200:
		r.raw.decode_content = True
		with open(filename, "wb") as f:
			shutil.copyfileobj(r.raw, f)
		print (f' Image {titre_image} téléchargée')
	else : 
		print (f'Image {titre_image} non téléchargée - problème laison URL')
	return data