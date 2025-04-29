interval_seconds = 30000000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger

# Watcher: field_value_missing


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



def run():
    elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
    elastic_user = "admin"
    elastic_pass = "temporal"

    now = datetime.utcnow()
    since = now - timedelta(hours=1)

    query = {
        "bool": {
            "must": [
                { "range": { "@timestamp": { "gte": since.isoformat(), "lt": now.isoformat() } }},
                { "term": { "status_code": "408" }}
            ]
        }
    }

    result = es.count(index="watcher-pruebas", body={ "query": query })

    if result['count'] == 0:
        logger.info("ALERTA: No se ha encontrado '408' en el campo 'status_code'.")
        # Webhooks
        send_elasticsearch_alert({"field_value_missing": " ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)