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

# Watcher: field_value_missing


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



# Definición de una función: run
def run():
    now = datetime.utcnow()
    since = now - timedelta(hours=1)

    query = {
        "bool": {
            "must": [
                { "range": { "@timestamp": { "gte": since.isoformat(), "lt": now.isoformat() } }},
                { "term": { "status_code": "405" }}
            ]
        }
    }

    result = es.count(index="watcher-pruebas", body={ "query": query })

    if result['count'] == 0:
        logger.info("ALERTA: No se ha encontrado '405' en el campo 'status_code'.")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "field_value_missing"})