Docker Compose Setup for Kafka, Elasticsearch, Kibana, Kafka Manager, Redis, and Redis Commander
This repository contains a Docker Compose setup to run the following services:

Zookeeper: Manages Kafka broker coordination.
Kafka: Message broker for handling publish-subscribe messaging.
Elasticsearch: Distributed search and analytics engine.
Kibana: Data visualization dashboard for Elasticsearch.
Kafka Manager: Web UI for managing Kafka clusters.
Redis: In-memory data structure store.
Redis Commander: Web-based GUI for managing Redis.
Prerequisites
Make sure you have Docker and Docker Compose installed on your machine.

Docker Installation Guide
Docker Compose Installation Guide
Usage
Clone the repository:

bash
Copy code
git clone [<repository-url>](https://github.com/tamnn25/TestService.git)
cd [<repository-directory>](https://github.com/tamnn25/TestService.git)
Start the services using Docker Compose:

bash
Copy code
docker-compose up -d
This command will download the necessary Docker images and start the services defined in the docker-compose.yml file.

Access the services:

Zookeeper: localhost:2181
Kafka: localhost:9092
Elasticsearch: http://localhost:9200
Kibana: http://localhost:5601
Kafka Manager: http://localhost:9000
Redis Commander: http://localhost:8081
Stop the services:

bash
Copy code
docker-compose down
Services Configuration
Zookeeper
Image: bitnami/zookeeper:3.7.0
Ports: 2181:2181
Environment Variables: ALLOW_ANONYMOUS_LOGIN: "yes"
Kafka
Image: wurstmeister/kafka:2.13-2.7.0
Ports: 9092:9092
Environment Variables:
makefile
Copy code
KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
Elasticsearch
Image: docker.elastic.co/elasticsearch/elasticsearch:7.13.3
Ports: 9200:9200
Environment Variables:
makefile
Copy code
discovery.type: single-node
cluster.name: docker-cluster
Kibana
Image: docker.elastic.co/kibana/kibana:7.13.3
Ports: 5601:5601
Environment Variables: ELASTICSEARCH_URL: http://elasticsearch:9200
Kafka Manager
Image: provectuslabs/kafka-ui:latest
Ports: 9000:8080
Environment Variables:
makefile
Copy code
KAFKA_CLUSTERS_0_NAME: docker-cluster
KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
Redis
Image: redis:latest
Ports: 6379:6379
Redis Commander
Image: rediscommander/redis-commander:latest
Ports: 8081:8081
Environment Variables: REDIS_HOSTS: "redis-dotnet:6379"