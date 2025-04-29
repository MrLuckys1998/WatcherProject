interval_seconds = 200000
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
            "avg_value": {
                "avg": {
                    "field": "latency"
                }
            }
        }
    })

    avg = result['aggregations']['avg_value']['value']
    if avg is not None and avg > 50:
        message = f"ALERTA: Promedio de 'latency' =  supera 50"
        logger.info(message)
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "avg_threshold"})