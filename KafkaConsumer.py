from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer('test-topic',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

es_host = 'http://localhost:9200'  # Including the protocol in the URL
es_index = 'topic'  # Index name in Elasticsearch

es = Elasticsearch([es_host])

for message in consumer:
    es.index(index='kafka-index', doc_type='_doc', body=message.value)
    print(f"Inserted: {message.value}")
