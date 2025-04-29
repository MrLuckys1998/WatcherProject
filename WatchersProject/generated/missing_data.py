interval_seconds = 300
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

# Watcher: missing_data


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



# Definición de una función: run
def run():
    now = datetime.utcnow()
    since = now - timedelta(hours=1)

    result = es.count(index="empty_index", body={
        "query": {
            "range": {
                "@timestamp": {
                    "gte": since.isoformat(),
                    "lt": now.isoformat()
                }
            }
        }
    })

    if result['count'] == 0:
        logger.info("ALERTA: No hay datos en la última hora.")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "missing_data"})