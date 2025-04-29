interval_seconds = 30000000
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

# Watcher: multi_field_values


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))


# Definición de una función: run
def run():
    now = datetime.utcnow()
    since = now - timedelta(minutes=30)

    conditions = [
        { "term": { cond["field"]: cond["value"] } } for cond in [{"field": "status", "value": 500}, {"field": "error", "value": "Timeout"}]
    ]

    query = {
        "bool": {
            "must": [
                { "range": { "@timestamp": { "gte": since.isoformat(), "lt": now.isoformat() } }},
                { "bool": { "should": conditions }}
            ]
        }
    }

    result = es.count(index="watcher-pruebas", body={ "query": query })

    count = result['count']
    if count > 0:
        logger.info(f"ALERTA: Detectadas {count} ocurrencias de condiciones definidas.")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "multi_field_values"})