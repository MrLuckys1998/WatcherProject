interval_seconds = 300000
# Importación de módulos necesarios
from logger import logger
# Importación de módulos necesarios
from utils import send_elasticsearch_alert

# Importación de módulos necesarios
from elasticsearch import Elasticsearch
# Importación de módulos necesarios
from datetime import datetime, timedelta
# Importación de módulos necesarios
from logger import logger

# Watcher: min_threshold


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



# Definición de una función: run
def run():
    now = datetime.utcnow()
    since = now - timedelta(minutes=30)

    result = es.search(index="watcher-pruebas", size=0, body={
        "query": {
            "range": {
                "@timestamp": {
                    "gte": since.isoformat(),
                    "lt": now.isoformat()
                }
            }
        },
        "aggs": {
            "min_value": {
                "min": {
                    "field": "temperature"
                }
            }
        }
    })

    value = result['aggregations']['min_value']['value']
    if value < 5:
        logger.info(f"ALERTA: MIN(temperature) =  < 5")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "min_threshold"})