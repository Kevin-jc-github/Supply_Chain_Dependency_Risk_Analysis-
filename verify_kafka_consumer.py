# verify_kafka_consumer.py

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'raw_dependencies',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("📡 Listening for messages from Kafka topic 'raw_dependencies'...")
for message in consumer:
    print("Received:", message.value)
