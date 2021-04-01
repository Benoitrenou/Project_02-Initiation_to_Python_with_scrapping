import requests
import re
from bs4 import BeautifulSoup 
from math import *



#Extraction urls des catégories dans une liste categories_urls
url = ("http://books.toscrape.com/index.html")
response = requests.get(url)
if response.ok : 
	soup = BeautifulSoup(response.text, "lxml")
	categories_urls = [x.get("href") for x in soup.find_all("a", href=re.compile("catalogue/category/books"))]
	categories_urls = categories_urls[1:]

#Print toutes les catégories pour permettre à utilisateur de choisir 
for y in categories_urls:
	print(f'Catégorie disponible : {y.replace("catalogue/category/books/", "").replace("/index.html", "")}')


#Choix catégorie par utilisateur et modif URL en conséquence 
categorie_choisie = input("Suivez les modèles proposés : nom_n° \nQuelle est la catégorie que vous recherchez ?")
url = f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/index.html"
print (url)

#Définition nombre de résultats/pages et modification url en conséquence
response = requests.get(url)
if response.ok : 
	soup = BeautifulSoup(response.text, "lxml")
	results = soup.find('form', {'class' : 'form-horizontal'}).find('strong').text
	nombre_pages = ceil(float(results) / 20)
	urls = []
	if nombre_pages != 1 :
		for i in range (1, nombre_pages+1) : 
			url = (f"http://books.toscrape.com/catalogue/category/books/{categorie_choisie}/page-{str(i)}.html")
			urls.append(url)
	else :
		urls.append (url)
#Liste urls_categ stock les urls des pages de la catégorie

# Recenser articles par catégorie
liens_articles = []
for j in urls:
	response = requests.get(j)
	if response.ok : 
		soup = BeautifulSoup(response.text, "lxml")	
		articles = soup.findAll("article")
		for article in articles:
			a = article.find("a")
			link = a["href"].replace("../../../", "")
			liens_articles.append(f"http://books.toscrape.com/catalogue/{link}")
print(f"Nombre de livres de cette catégorie : {len(liens_articles)}")
# Liste liens_articles stock les urls de chaque article


books = [] 
for url in liens_articles : 
	response = requests.get(url) 
	if response.ok : 
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "lxml")
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
		books.append(data)
#liste books de listes datas qui contiennent infos de chaque livre

print (len(books))
print (books)

