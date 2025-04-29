interval_seconds = 3000000
# Importación de módulos necesarios
from logger import logger
# Importación de módulos necesarios
from utils import send_elasticsearch_alert

# Importación de módulos necesarios
from elasticsearch import Elasticsearch
# Importación de módulos necesarios
from logger import logger
# Importación de módulos necesarios
from datetime import datetime, timedelta


# Watcher: ratio_between_fields


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



# Definición de una función: run
def run():
    now = datetime.utcnow()
    since = now - timedelta(minutes=15)

    result = es.search(index="watcher-pruebas", size=0, body={
        "query": { "range": { "@timestamp": { "gte": since.isoformat(), "lt": now.isoformat() } }},
        "aggs": {
            "num": { "sum": { "field": "errors" }},
            "den": { "sum": { "field": "requests" }}
        }
    })

    num = result['aggregations']['num']['value']
    den = result['aggregations']['den']['value']
    if den and (num / den) > 0.1:
        logger.info(f"ALERTA: Ratio {num}/{den} = {num/den} > 0.1")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "ratio_between_fields"})