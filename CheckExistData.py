from confluent_kafka import Consumer, KafkaException
from elasticsearch import Elasticsearch, exceptions as es_exceptions
import json

# Elasticsearch configuration
es_host = 'http://192.168.1.12:9200'  # Including the protocol in the URL
es_index = 'topic'  # Index name in Elasticsearch
es_username = 'elastic'  # Replace with your Elasticsearch username
es_password = '123changeme'  # Replace with your Elasticsearch password

print("Connecting to Elasticsearch at:", es_host)

# Create Elasticsearch client
es_client = Elasticsearch([es_host], http_auth=(es_username, es_password))

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

# Function to check if a document already exists in Elasticsearch
def document_exists(data_id):
    try:
        res = es_client.exists(index=es_index, id=data_id)
        return res
    except es_exceptions.ConnectionError as e:
        print("Failed to check document: Connection error", e)
        return False
    except es_exceptions.TransportError as e:
        print("Failed to check document: Transport error", e)
        return False
    except Exception as e:
        print("Failed to check document: An error occurred", e)
        return False

# Kafka consumer configuration
conf = {
    'bootstrap.servers': '192.168.1.12:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'  # Start consuming from the earliest message
}

# Create Kafka consumer
consumer = Consumer(conf)

# Subscribe to Kafka topic(s)
topic = 'subscribers'
consumer.subscribe([topic])

# Function to process existing messages
def process_existing_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                break
            if msg.error():
                print(msg.error())
                continue

            # Process message
            data = json.loads(msg.value().decode('utf-8'))  # Assuming messages are JSON

            print(12121212)
            print(data)
            data_id = data.get("id")  # Assuming each message has a unique "id"
            if data_id and not document_exists(data_id):
                index_to_es(data)
    except Exception as e:
        print("Failed to process existing messages:", e)
    finally:
        consumer.close()

# Process existing messages before starting the continuous event listening
# process_existing_messages()

# def consume_all_messages():
#     try:
#         while True:
#             msg = consumer.poll(timeout=1.0)
#             if msg is None:
#                 break  # No more messages
#             if msg.error():
#                 print(f"Consumer error: {msg.error()}")
#                 continue

#             # Process message
#             data = json.loads(msg.value().decode('utf-8'))  # Assuming messages are JSON
#             print("Received message:", data)
#             # Here you can process the data as needed

#     except KafkaException as e:
#         print(f"Kafka exception: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         print("Done")
#         consumer.close()

# # Consume all messages from the Kafka topic
# consume_all_messages()

def sync_kafka_to_es():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            # Process message
            data = json.loads(msg.value().decode('utf-8'))  # Assuming messages are JSON
            data_id = data.get("id")  # Assuming each message has a unique "id"
            if data_id and not document_exists(data_id):
                index_to_es(data, data_id)
    except KafkaException as e:
        print("KafkaException occurred: ", e)
    except json.JSONDecodeError as e:
        print("JSONDecodeError occurred: ", e)
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        consumer.close()

# Sync Kafka data to Elasticsearch
sync_kafka_to_es()

def list_all_indices():
    try:
        indices = es_client.cat.indices(format='json')
        print("List of indices in Elasticsearch:")
        for index in indices:
            print(index['index'])
    except es_exceptions.ConnectionError as e:
        print("Failed to list indices: Connection error", e)
    except es_exceptions.TransportError as e:
        print("Failed to list indices: Transport error", e)
    except Exception as e:
        print("Failed to list indices: An error occurred", e)

# Call the function to list all indices
# list_all_indices()