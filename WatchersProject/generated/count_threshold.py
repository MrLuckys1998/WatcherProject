interval_seconds = 300000
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
    if count > 6 :
        message = f"ALERTA: Número de documentos =  > 10"
        logger.info(message)
        # Webhooks
        send_elasticsearch_alert({"count_threshold": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)
