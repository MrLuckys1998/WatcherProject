interval_seconds = 3000000
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

# Watcher: sum_threshold


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
            "total_sum": {
                "sum": {
                    "field": "duration"
                }
            }
        }
    })

    value = result['aggregations']['total_sum']['value']
    if value > 999:
        logger.info(f"ALERTA: SUM(duration) =  > 999")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "sum_threshold"})