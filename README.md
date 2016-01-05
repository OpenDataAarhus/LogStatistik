#Logstatistics  
  
Installation    
  
1 crontab 59 23 * * * sudo bash .../LogStatistics/LogStatistics.sh   
2 Files LogStatistics.db LogStatistics.py LogStatistics.sh  
Loading it into the same folder example.../LogStatistics
  
#Documentation  
  
LogStatistics uses the CKAN log file: ckan_default.custom.log  
  
It is a two phase process:  
  
Step 1   
  
It collects all the logs, which contains api and downloads.  
  
The logs which contains "/action/datastore_search?resource_id=" will be saved in the file ckanapi.log
The logs which contains "GET /dataset/" will be saved in the file download.log
Step 2
The log files will be saved in the database in the database LogStatistics.db
The ckanapi.log file will be saved in the table ckanapi in the database LogStatistics.db.
The download.log file will be saved in the table download in the database LogStatistics.db.
This way it is easy to work with the numbers, sort them, use them in statistics and so on. 
The result of this will be transferred to your CKAN.
