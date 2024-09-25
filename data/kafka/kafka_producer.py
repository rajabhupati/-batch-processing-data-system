from kafka import KafkaProducer, KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import json
import time

# JSON Serializer for the data
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Function to create topic if not exists
def create_kafka_topic(topic_name):
    admin_client = KafkaAdminClient(bootstrap_servers=['kafka:9092'])
    topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print(f"Topic '{topic_name}' created.")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists.")
    finally:
        admin_client.close()

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=json_serializer)

# Create topic 'taxi_trips' if it doesn't exist
create_kafka_topic('taxi_trips')

# Sample Data to be produced
data = {"trip_id": 1, "duration": 20, "passenger_count": 2}

# Producing data to the topic
for _ in range(100):
    producer.send('taxi_trips', data)
    time.sleep(1)  # Simulate producing data every second
