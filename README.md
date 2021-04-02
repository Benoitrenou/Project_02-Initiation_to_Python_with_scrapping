Afin de faire fonctionner ce script, veuillez suivre les étapes suivantes 

1. Installer les packages précisés dans requirements
2. Lancer le script désiré depuis le terminal 
  - Pour le script 'scrap_url.py' : veuillez copier-coller l'URL du livre sur books.toscrape.com dont vous désirez récupérer les données
  exemple : http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
  > le script crée un fichier csv dans lequel sont écrites les données du livre nommé d'après le titre du livre
  > le script télécharge l'image de la couverture du livre nommée d'après le titre du livre 
  
  - Pour le script 'scrap_categorie.py' : entrez la catégorie dont vous désirez récupérer les données sur le modèle 'catégorie_n°'
  Le script énumère toutes les catégories et le n° correspondant, il vous suffit de choisir au sein de cette liste 
  exemple : poetry_23
  > le script crée un fichier csv nommé selon la catégorie choisie dans lequel sont écrites les données de tous les livres de la catégorie 
  > le script télécharge chaque couverture qui sont nommées d'après le titre du livre
  
  - Pour le script 'scrap_général.py' : lancez simplement le script pour que celui-ci récupère les données de l'ensemble des livres du site 
  > le script crée un fichier csv pour chaque catégorie dans lequel sont écrites les données de tous les livres de la catégorie  
  > le script télécharge chaque couverture qui sont nommées d'après le titre du livre
