This project aims to be a first introduction to the Python language
The objective of the project scenario is to set up a python script to retrieve data from the site https://books.toscrape.com/

Notions to master :
    - Set up a Python virtual environment
    - Mastery of the packages Requests, BeautifulSoup
    - Data retrieving, cleaning and writing
    - Writing a CSV file

## Create virtual envrionment

### With Linux / Mac OS

    $ python -m venv <environment_name>
    example : python -m venv env_scrapping

### With Windows

    $ virtualenv <environment_name>
    example : virtualenv env_scrapping

## Activate virtual environment

### With Linux / Mac OS

    $ source <environment_name>/bin/activate
    exemple : source env_scrapping/bin/activate

### With Windows

    $ source <environment_name>/Scripts/activate
    exemple : source env_scrapping/Scripts/activate

## Installation of packages

    $ pip install -r requirements.txt

## Use of scripts

To run the desired script from the terminal, use the command : 

    $ python <script_name>
    example : $ python scrap_url.py

There are three scripts available;
    - scrap_url.py to retrieve data of one particular book
    - scrap_categorie.py to retrieve data of one category's books
    - scrap_general.py to retreive data froç the entire site

Here is how to use each of them:

## A. For scrap_url.py : 

Copy-Paste URL of the book on the site books.toscrap.com

    example : http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html

The script opens a directory named with the targeted book and the date and time of the script execution

    example : C:\...\fichiers-A Light in the Attic-2021-04-19_14-24-58

The script downloads a .csv file containing the data of the targeted book to the directory

    example : C:\...\fichiers-A Light in the Attic-2021-04-19_14-24-58/Data-A Light in the Attic.csv

The script downloads a .jpeg file of the target book cover image to the directory

    example : C:\...\fichiers-A Light in the Attic-2021-04-19_14-24-58/Image_A Light in the Attic_Poetry.jpeg

## B. For scrap_categorie.py : 

Enter the category from which you want to retrieve data following the template indicated "category_name_n°"

    example : travel_2

The script creates a directory named with the target category and the date and time of the script execution

    example : C:\...\fichiers-travel_2-2021-04-19_13-54-10

The script downloads a .csv file containing the data of all the books of the targeted category in the directory

    example : C:\...\fichiers-travel_2-2021-04-19_13-54-10/Data-travel_2.csv

The script downloads the .jpeg files of the cover images of all the books of the targeted category in the directory

    example : C:\...\fichiers-travel_2-2021-04-19_13-54-10/Image_*.jpeg

## C. For scrap_general.py : 

Run the script that will perform the same process as scrap_categorie.py but for each category of the site 
A directory is created for each of them