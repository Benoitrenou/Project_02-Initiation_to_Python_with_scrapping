from bs4 import BeautifulSoup
import requests
import re
import csv
import shutil
from math import ceil
from pathvalidate import sanitize_filename
from pathvalidate import sanitize_filepath
import datetime
import os

def make_soup(url):
    response = requests.get(url)
    result = response.content.decode("utf8")
    soup = BeautifulSoup(result, "lxml")
    return soup

class Site:

	url = 'https://books.toscrape.com/'

	def __init__(self):
		soup = make_soup(self.url) #self.url = meilleure manière d'accéder à attribut de classe ?
		self.categories = [
		x.get("href")
		for x in soup.find_all("a", href=re.compile("catalogue/category/books"))
		]
		self.categories = self.categories [1:]

	def present_categories (self):
		for y in self.categories:
			print(f'Catégorie disponible : {y.split("/")[3]}')

	def scrap (self):
		for categ in self.categories:
			category = Category ()
			directory = Directory (f'{categ.split("/")[3]}')
			category.scrap_books_of_category (f'{categ.split("/")[3]}', directory.give_path())
			category.write_csv(directory.give_path())

	@classmethod 
	# Pas d'intérêt pratique ici mais juste pour montrer utilisation éventuelle d'une méthode de classe
	def change_url (cls, url):
		cls.url = url

class Directory:
	def __init__ (self, titre):
		date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		self.titre = f'{titre:.60}'
		titre_file = sanitize_filepath(self.titre)
		self.path = f"{os.getcwd()}/{titre_file}-{date}"
		os.mkdir(self.path)
		print(f"Dossier d'enregistrement des fichiers : {self.path}\n")


	def give_path (self):
		return self.path

class Category:
	def __init__(self):
		self.category = []

	def scrap_books_of_category (self, choice, path):
		self.choice = choice
		category_url = f'https://books.toscrape.com/catalogue/category/books/{self.choice}/index.html'
		soup = make_soup(category_url)
		results = soup.find("form", {"class": "form-horizontal"}).find("strong").text
		nombre_pages = ceil(float(results) / 20)
		category_urls = []
		if nombre_pages != 1:
			for i in range(1, nombre_pages+1):
				url = f"http://books.toscrape.com/catalogue/category/books/{choice}/page-{str(i)}.html"
				category_urls.append(url)
		else:
			category_urls.append(category_url)
		books_urls = []
		for j in category_urls :
			soup = make_soup(j)
			books = soup.findAll("article")
			for book in books:
				a = book.find("a")
				url = a["href"].replace("../../../", "")
				books_urls.append(f"http://books.toscrape.com/catalogue/{url}")
		print(f"\nNombre de livres de cette catégorie : {len(books_urls)}\n")
		self.books_data = []
		for book in books_urls:
			book = Book (book)
			book.download_cover(path)
			self.books_data.append(book.data)

	def write_csv (self, path):
		self.csv = Excel(self.choice).write(path, self.books_data)

class Book:
	def __init__ (self, url):
		soup = make_soup(url)
		self.title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text.replace("’", " ").replace('"', ' ')
		self.categorie = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[2].text.replace("\n", "")
		self.upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0].text
		self.cover_url = f'http://books.toscrape.com/{soup.find("img")["src"]}'
		self.data = [self.title, self.categorie, self.upc, self.cover_url]

	def write_csv (self, path):
		self.csv = Excel(sanitize_filename(self.title)).write(path, [self.data])

	def download_cover (self, path):
		self.cover = Cover (path, sanitize_filename(self.title), self.cover_url)

class Excel: 
	ENTETE = ["Titre","Catégorie","UPC", "URL Couverture"]

	def __init__(self, title):
		self.title = f'fichier-{title}.csv'

	def write (self, path, liste):
		with open(f'{path}/{self.title}', "w", encoding="utf-8-sig", newline="") as file :
			self.writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=";")
			self.writer.writerow(Excel.ENTETE)
			self.writer.writerows(liste)

class Cover:
	def __init__(self, path, title, cover_url):
		self.title = f'{title:.60}.jpeg'
		r = requests.get(cover_url, stream=True)
		if r.status_code == 200:
			r.raw.decode_content = True
			with open(f'{path}/{self.title}', "wb") as f:
				shutil.copyfileobj(r.raw, f)


def scrap_livre() : 
	book = Book (input ('Url de votre livre : '))
	print (f'Livre analysé : {book.title}')
	directory = Directory (book.title)
	book.write_csv(directory.give_path())
	print (f'Données de {book.title}')
	book.download_cover(directory.give_path())
	print (f'Couverture de {book.title} téléchargée')

def scrap_category() : 
	category = Category ()
	category_choice = input ('Quel categorie ?')
	directory = Directory (category_choice)
	category.scrap_books_of_category (category_choice, directory.give_path())
	category.write_csv(directory.give_path())

choix = input ('1-livre / 2-catégorie : 3-toutes les catégories')
if choix == '1' : 
	scrap_livre()
if choix == '2' :
	site = Site ()
	site.present_categories()
	scrap_category ()
if choix == '3' : 
	site = Site ()
	site.scrap ()
else :
	print ('Choix incompris')