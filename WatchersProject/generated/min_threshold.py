interval_seconds = 300000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger

# Watcher: min_threshold


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



def run():
    elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
    elastic_user = "admin"
    elastic_pass = "temporal"
    
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
        # Webhooks
        send_elasticsearch_alert({"min_threshold": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)