# producer/kafka_producer.py
from kafka import KafkaProducer
from sensor_simulator import generate_sensor_data
import json

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['172.31.109.162:9092'],  # Use your WSL IP
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Send fake SCADA data to Kafka topic "scada-sensor-data"
for data in generate_sensor_data():
    producer.send('scada-sensor-data', data)
    print(f"Sent: {data}")