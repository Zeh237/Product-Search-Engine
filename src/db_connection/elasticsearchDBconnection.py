import os
from elasticsearch import Elasticsearch
import logging

logging.basicConfig(level=logging.INFO)

class ElasticsearchDBConnection:
    host = os.getenv("ES_HOST")
    username = os.getenv("ES_USERNAME")
    password = os.getenv("ES_PASSWORD")
    port = os.getenv("ES_PORT")

    def __init__(self):
        self.es = Elasticsearch(
            [self.host],
            basic_auth=(self.username, self.password),
            verify_certs=False
        )

    def es_connection(self):
        return self.es

