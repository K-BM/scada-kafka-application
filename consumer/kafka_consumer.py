# consumer/kafka_consumer.py
from kafka import KafkaConsumer
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, DateTime, MetaData
import json
import datetime

# PostgreSQL connection (from your requirements.txt)
engine = create_engine('postgresql://scada_user:scada_pass@172.31.109.162:5432/scada_db')
metadata = MetaData()

# Define the sensor_data table (same as earlier steps)
sensor_data = Table(
    'sensor_data', metadata,
    Column('id', Integer, primary_key=True),
    Column('timestamp', DateTime),
    Column('sensor_id', String),
    Column('temperature', Float),
    Column('pressure', Float),
    Column('flow_rate', Float),
    Column('status', String)
)
metadata.create_all(engine)  # Create table if not exists

# Kafka consumer setup
consumer = KafkaConsumer(
    'scada-sensor-data',
    bootstrap_servers=['172.31.109.162:9092'],  # Your WSL IP
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest'
)

# Insert data into PostgreSQL
print("Consumer started...")
for message in consumer:
    data = message.value
    try:
        with engine.connect() as conn:
            conn.execute(sensor_data.insert().values(
                timestamp=datetime.datetime.fromtimestamp(data['timestamp']),
                sensor_id=data['sensor_id'],
                temperature=data['temperature'],
                pressure=data['pressure'],
                flow_rate=data['flow_rate'],
                status=data['status']
            ))
            conn.commit()
        print(f"Inserted: {data}")
    except Exception as e:
        print(f"ERROR: {e}")