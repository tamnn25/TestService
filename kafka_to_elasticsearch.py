from confluent_kafka import Consumer, KafkaException
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import json

# Elasticsearch configuration
es_host = 'http://localhost:9200'  # Including the protocol in the URL
es_index = 'topic-1'  # Index name in Elasticsearch

print("Connecting to Elasticsearch at:", es_host)


# Create Elasticsearch client
es_client = Elasticsearch([es_host])

# Function to index data into Elasticsearch
def index_to_es(data):
    try:
        res = es_client.index(index=es_index, body=data)
        print("Indexed data:", res)
    except es_exceptions.ConnectionError as e:
        print("Failed to index data: Connection error", e)
    except es_exceptions.TransportError as e:
        print("Failed to index data: Transport error", e)
    except Exception as e:
        print("Failed to index data: An error occurred", e)

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'  # Start consuming from the earliest message
}

# Create Kafka consumer
consumer = Consumer(conf)

# Subscribe to Kafka topic(s)
topic = 'topic-a'
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue

        # Process message
        data = json.loads(msg.value().decode('utf-8'))  # Assuming messages are JSON
        print("Received message:", data)
        # Call function to sync data to Elasticsearch
        index_to_es(data)

finally:
    consumer.close()
