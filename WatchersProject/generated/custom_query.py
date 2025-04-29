interval_seconds = 300000
from logger import logger
from utils import send_elasticsearch_alert

"""
Watcher: custom_query
Descripción: Ejecuta una consulta personalizada definida completamente por el usuario.
Parámetros esperados:
- index: Índice de Elasticsearch
- query: Objeto completo de la query
- condition_script: (opcional) Código Python que evalúa si se dispara la alerta
- elastic_url, elastic_user, elastic_pass
"""

from elasticsearch import Elasticsearch
from datetime import datetime
from logger import logger

# Conexión a Elasticsearch

es = Elasticsearch("https://wtslcccelkp0050.unix.wtes.corp:9200", basic_auth=("admin", "temporal"), verify_certs=False)


def run():
    try:
        elastic_url = "https://wtslcccelkp0050.unix.wtes.corp:9200"
        elastic_user = "admin"
        elastic_pass = "temporal"

        # Ejecutar búsqueda usando una query personalizada
        result = es.search(index="watcher-pruebas*", body={"query": {"range": {"@timestamp": {"gte": "now-30m"}}}})
        logger.info("Consulta ejecutada")

        
        # Evaluar la condición definida por el usuario
        try:

            if result['hits']['total']['value'] > 0 :
              # Webhooks
              send_elasticsearch_alert({"custom_query": "ok"}, es_url=elastic_url, user=elastic_user, password=elastic_pass)

        except Exception as ce:
            logger.error(f"Error evaluando condición: {ce}")
        

    except Exception as e:
        logger.error(f"Error durante la ejecución del watcher: {e}")
