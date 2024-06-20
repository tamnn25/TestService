from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic, message):
    producer.send(topic, message)
    producer.flush()

# Simulate sending messages
for i in range(10):
    i += 50
    message = {'id': i, 'value': f'Message {i}'}
    send_message('topic', message)
    time.sleep(1)
