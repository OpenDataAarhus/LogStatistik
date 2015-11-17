sudo grep "GET /dataset/" /var/log/apache2/ckan_default.custom.log >/home/deploy/bin_script/LogStatistik/download.log
sudo grep "/action/datastore_search?resource_id=" /var/log/apache2/ckan_default.custom.log  >/home/deploy/bin_script/LogStatistik/ckanapi.log
python /home/deploy/bin_script/LogStatistik/LogStatistik.py
