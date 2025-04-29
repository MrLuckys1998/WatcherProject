interval_seconds = 300000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger
import json

# Watcher: unique_terms_missing
# Descripción: Agrupa por un campo (ej: service.keyword) y alerta si alguno de los valores esperados no aparece.





es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))


def run():
    elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
    elastic_user = "admin"
    elastic_pass = "temporal"
    
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
    expected_terms_data = json.loads('''["servicioA", "servicioB", "servicioC"]''')
    missing = [term for term in expected_terms_data if term not in terms]

    if missing:
      logger.info(f"ALERTA: No se han detectado los términos esperados: {missing}")
      # Webhooks
      send_elasticsearch_alert({"unique": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)
