#Logstatistics  
(http://www.odaa.dk/dataset/statistik-pa-odaa/resource/caf6cb0f-a241-459b-a045-a54fad7ebe3a)
  
Installation    
  
1   crontab 59 23 * * * sudo bash .../LogStatistics/LogStatistics.sh   
2   Files LogStatistics.db LogStatistics.py LogStatistics.sh  
    Loading it into the same folder example.../LogStatistics
  
#Documentation  
  
LogStatistics uses the CKAN log file: ckan_default.custom.log  
  
It is a two phase process:  
  
Step 1   
  
1.   It collects all the logs, which contains api and downloads.  
2.   The logs which contains "/action/datastore_search?resource_id=" will be saved in the file ckanapi.log   
3.   The logs which contains "GET /dataset/" will be saved in the file download.log  
  
Step 2  
  
1.  The log files will be saved in the database in the database LogStatistics.db
2.  The ckanapi.log file will be saved in the table ckanapi in the database LogStatistics.db.
3.  The download.log file will be saved in the table download in the database LogStatistics.db.  
  
This way it is easy to work with the numbers, sort them, use them in statistics and so on. 
  
The result of this will be transferred to your CKAN.

#resource.py
http://www.odaa.dk/dataset/statistik-pa-odaa/resource/c81046d7-5071-4e42-aa5d-ed949bcfc250   
Display a list of all active dataset.

