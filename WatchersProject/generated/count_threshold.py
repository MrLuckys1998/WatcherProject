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
    since = now - timedelta(minutes=40)

    result = es.count(index="watcher-pruebas", body={
        "query": {
            "range": {
                "@timestamp": {
                    "gte": since.isoformat(),
                    "lt": now.isoformat()
                }
            }
        }
    })

    count = result['count']
    if count > 1:
        message = f"ALERTA: Número de documentos =  > 1"
        logger.info(message)
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "count_threshold"})