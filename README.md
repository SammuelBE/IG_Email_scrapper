# Instagram Email Scrapper
Récupère les e-mails des utilisateurs ayant posté avec un certain hashtag et inscrit les e-mails dans un fichier csv.

### Requis :
- Sessions IDs 
- Python 3

### Optionnel :

- Proxy

### Variables :
- Hashtag ([TAG](https://github.com/SammuelJ/IG_Email_scrapper/blob/master/ig_scrap.py#L15)) - default 'fitness'
- Nombre minimum de followers ([MIN_FOLLOWERS](https://github.com/SammuelJ/IG_Email_scrapper/blob/master/ig_scrap.py#L16)) - default '10'

### A faire :
- Docstring
- Optimiser la facon dont le scrap fonctionne

### Problemes :
- Lorsque le script crash, celui-ci redémarre de zero (On retombe sur les memes users donc pas opti)
- Crash pour une raison inconnue (Json parsing ?..?)

### Lancement

Vous pouvez modifier les variables TAG (string) ainsi que MIN_FOLLOWERS (int) afin d'affiner le scrapping.

Démarrer le script
``` python ig_scrap.py ```
