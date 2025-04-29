interval_seconds = 30000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger


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
            "avg_value": {
                "avg": {
                    "field": "latency"
                }
            }
        }
    })

    avg = result['aggregations']['avg_value']['value']
    if avg is not None and avg > 1:
        message = f"ALERTA: Promedio de 'latency' =  supera 1"
        logger.info(message)
        # Webhooks
        send_elasticsearch_alert({"avg_threshold": "okey"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)