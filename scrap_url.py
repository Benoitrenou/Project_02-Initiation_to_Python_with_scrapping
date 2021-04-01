import requests
import re
from bs4 import BeautifulSoup 
from fonctions_scrap import getresponseandsoup 
from fonctions_scrap import getbookdata

url = input ('URL de votre livre : ')

data = getbookdata (url) 
print (data)