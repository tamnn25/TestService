from kafka import KafkaAdminClient
from kafka import KafkaConsumer

admin_client = KafkaAdminClient(
    bootstrap_servers="192.168.1.12:9092", 
    client_id='test'
)

topics = admin_client.list_topics()

print(topics)

# for topic in topics:
#     consumer = KafkaConsumer(
#         topic,
#         bootstrap_servers='localhost:9092',
#         auto_offset_reset='earliest',  # Start reading at the earliest message
#         enable_auto_commit=True,       # Commit offsets automatically
#         group_id='my-group',           # Consumer group ID
#         value_deserializer=lambda x: x.decode('utf-8')  # Decode messages as UTF-8 strings
#     )

#     print(f"Consuming messages from topic: {topic}")

#     # Consume messages
#     for message in consumer:
#         print(f"Received message: {message.value}")

# print(topics)

# Function to consume messages from a topic
def consume_topic(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',  # Start reading at the earliest message
        enable_auto_commit=True,       # Commit offsets automatically
        group_id='my-group',           # Consumer group ID
        value_deserializer=lambda x: x.decode('utf-8')  # Decode messages as UTF-8 strings
    )

    print(f"Consuming messages from topic: {topic}")
    for message in consumer:
        print(f"Topic: {message.topic}, Partition: {message.partition}, Offset: {message.offset}, Key: {message.key}, Value: {message.value}")
        # For demonstration purposes, we'll break after reading a few messages
        # Remove the below break statement to read all messages
        break

# Consume messages from each topic
# for topic in topics:
#     consume_topic(topic)

