interval_seconds = 3000000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger

# Watcher: missing_data


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



def run():
    elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
    elastic_user = "admin"
    elastic_pass = "temporal"

    now = datetime.utcnow()
    since = now - timedelta(hours=1)

    result = es.count(index="test_missing", body={
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
        # Webhooks
        send_elasticsearch_alert({"missing_data": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)