sort --field-separator=',' -u -k 10,10 dati.csv | awk -F "," '{print $10}'
