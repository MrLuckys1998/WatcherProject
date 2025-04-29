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

# Watcher: unique_terms_missing
# Descripción: Agrupa por un campo (ej: service.keyword) y alerta si alguno de los valores esperados no aparece.


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))


# Definición de una función: run
def run():
    now = datetime.utcnow()
    since = now - timedelta(hours=1)

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
            "unique_terms": {
                "terms": {
                    "field": "service.keyword",
                    "size": 100
                }
            }
        }
    })

    terms = [bucket['key'] for bucket in result['aggregations']['unique_terms']['buckets']]
    missing = [term for term in ["servicioA", "servicioB", "servicioC"] if term not in terms]
    if missing:
        logger.info(f"ALERTA: No se han detectado los términos esperados: {missing}")
        send_elasticsearch_alert({"Prueba": "OK!", "Watcher": "unique_terms_missing"})