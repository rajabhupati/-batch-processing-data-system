from kafka import KafkaConsumer
import json

# JSON Deserializer for the consumer
def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

# Kafka Consumer
consumer = KafkaConsumer(
    'taxi_trips',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='taxi_group',
    value_deserializer=json_deserializer
)

# Consuming the data
print("Starting consumer...")

for message in consumer:
    print(f"Received: {message.value}")
