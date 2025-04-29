interval_seconds = 300000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger

# Watcher: sum_threshold


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
            "total_sum": {
                "sum": {
                    "field": "duration"
                }
            }
        }
    })

    value = result['aggregations']['total_sum']['value']
    if value > 10:
        logger.info(f"ALERTA: SUM(duration) =  > 10")
        # Webhooks
        send_elasticsearch_alert({"sum_threshold": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)