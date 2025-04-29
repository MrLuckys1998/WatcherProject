interval_seconds = 3000000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger

# Watcher: ratio_between_fields


es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"))



def run():

    elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
    elastic_user = "admin"
    elastic_pass = "temporal"
    
    now = datetime.utcnow()
    since = now - timedelta(minutes=15)

    result = es.search(index="watcher-pruebas", size=0, body={
        "query": { "range": { "@timestamp": { "gte": since.isoformat(), "lt": now.isoformat() } }},
        "aggs": {
            "num": { "sum": { "field": "errors" }},
            "den": { "sum": { "field": "requests" }}
        }
    })

    num = result['aggregations']['num']['value']
    den = result['aggregations']['den']['value']
    if den and (num / den) > 0.1:
        logger.info(f"ALERTA: Ratio {num}/{den} = {num/den} > 0.1")
        # Webhooks
        send_elasticsearch_alert({"ratio_between_fields": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)