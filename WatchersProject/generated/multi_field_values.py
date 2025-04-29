interval_seconds = 3000000
from logger import logger
from utils import send_elasticsearch_alert

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from logger import logger
import json

# Watcher: multi_field_values





es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"), verify_certs=False)


def run():
    elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
    elastic_user = "admin"
    elastic_pass = "temporal"

    now = datetime.utcnow()
    since = now - timedelta(minutes=30)

    try:
        conditions_data = json.loads('''[{"field": "status", "value": 500}, {"field": "error", "value": "Timeout"}]''')
        conditions = [ { "term": { c["field"]: c["value"] } } for c in conditions_data ]
    except Exception as parse_err:
        logger.error(f"Error procesando condiciones: {parse_err}")
        return

    query = {
        "bool": {
            "must": [
                { "range": { "@timestamp" : { "gte": since.isoformat(), "lt": now.isoformat() } }},
                { "bool": { "should": conditions }}
            ]
        }
    }

    try:
        result = es.count(index="watcher-pruebas", body={ "query": query })
        count = result.get('count', 0)

        if count > 0:
            logger.info(f"ALERTA: Detectadas {count} ocurrencias de condiciones definidas.")
            # Webhooks
            send_elasticsearch_alert({"multi_field_values": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)

    except Exception as e:
        logger.error(f"Error durante la ejecución del watcher: {e}")
