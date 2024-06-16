from kafka import KafkaAdminClient

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092", 
    client_id='test'
)

topics = admin_client.list_topics()
print(topics)
