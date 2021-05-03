Afin de faire fonctionner ces scripts, veuillez suivre les étapes suivantes

Tout d'abord, clônez en local le dépôt distant

    $ git clone https://github.com/Benoitrenou/projet_02.git    

# I. Installation de l'environnement virtuel 

Si vous êtes sur un OS hors Windows 

Depuis votre terminal de commande, effectuez les commandes suivantes 

## Création de l'environnement virtuel : 

### Sous Linux/ MAC OS

    $ python -m venv <environment_name>
    exemple : python -m venv env_scrapping 
    
### Sous Windows:
    
    $ virtualenv <environment_name>
    exemple : virtualenv env_scrapping 
    
## Activation de l'environnement virtuel : 

### Sous Linux / MAC OS:

    $ source <environment_name>/bin/activate
    exemple : source env_scrapping/bin/activate
   
### Sous Windows:

    $ source <environment_name>/Scripts/activate
    exemple : source env_scrapping/Scripts/activate
    
## Installation des packages : 

    $ pip install -r requirements.txt
    
# II. Utilisation des scritps 

Pour lancer le script désiré depuis le terminal, utilisez la commande : 

    $ python <nom_du_script>
    exemple : $ python scrap_url.py

## A. Pour le script scrap_url.py : 

Copier-Coller l'URL du livre sur books.toscrap.com

    exemple : http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
    
Le script ouvre un répertoire comprenant le nom du livre visé et la date et l'heure de l'exécution du script

    exemple : C:\...\fichiers-A Light in the Attic-2021-04-19_14-24-58
    
Le script télécharge un fichier .csv contenant les données du livre ciblé dans le répertoire

    exemple : C:\...\fichiers-A Light in the Attic-2021-04-19_14-24-58/Data-A Light in the Attic.csv
    
Le script télécharge un fichier .jpeg de l'image de couverture du livre ciblé dans le répertoire

    exemple : C:\...\fichiers-A Light in the Attic-2021-04-19_14-24-58/Image_A Light in the Attic_Poetry.jpeg

## B. Pour le script scrap_categorie.py : 

Entrez la catégorie dont vous désirez récupérer les données en suivant le modèle indiqué "nomcatégorie_n°"

    exemple : travel_2
    
Le script crée un répertoire du nom de la catégorie visée et la date et l'heure de l'exécution du script

    exemple : C:\...\fichiers-travel_2-2021-04-19_13-54-10
    
Le script télécharge un fichier .csv contenant les données de tous les livres de la catégorie ciblée dans le répertoire

    exemple : C:\...\fichiers-travel_2-2021-04-19_13-54-10/Data-travel_2.csv
    
Le script télécharge les fichiers .jpeg des images de couvertures de tous les livres de la catégorie ciblée  dans le répertoire

    exemple :  exemple : C:\...\fichiers-travel_2-2021-04-19_13-54-10/Image_*.jpeg
    
## C. Pour le script scrap_general.py : 

Lancez le script qui effectuera le même process que scrap_categorie.py mais pour chaque catégorie du site 
Un répertoire est créé pour chacune d'entre elles 
