# LogStatistik

Installation

1. Setup crontab
	59 23 * * * sudo bash .../LogStatistik/LogStatistik.sh	

2. Files
	LogStatistik.db
	LogStatistik.py
	LogStatistik.sh

   Ligges ind i samme folder eks. ../LogStatistik

Dokumentation
------------------------
LogStatistik bruger ckan log filen ckan_default.custom.log
1. Hvor den samler alle de logs, som indeholder api og download.
       De logs som indeholder "/action/datastore_search?resource_id=" bliver gemt i filen ckanapi.log
       De logs som indeholder "GET /dataset/" bliver gemt i filen download.log

2. Log filerne bliver gemt i databasen LogStatistik.db
       ckanapi.log filen bliver gemt i tabellen ckanapi.
       download.log filen bliver gemt i tabellen download.
   Dette bliver gjort for at kunne lave forespørgsler på logs.

3. Resultatet bliver lagt over på CKAN.
