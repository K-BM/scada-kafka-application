import time
import random
from faker import Faker

fake = Faker()

# Create a fixed list of sensor IDs
NUM_SENSORS = 5
sensor_ids = [fake.uuid4() for _ in range(NUM_SENSORS)]

def generate_sensor_data():
    while True:
        data = {
            "timestamp": int(time.time()),
            "sensor_id": random.choice(sensor_ids),  # Randomly pick from fixed list
            "temperature": round(random.uniform(20.0, 100.0), 2),  # °C
            "pressure": round(random.uniform(1.0, 10.0), 2),       # bar
            "flow_rate": round(random.uniform(0.5, 5.0), 2),       # m³/s
            "status": random.choice(["NORMAL", "WARNING", "ALARM"])
        }
        yield data
        time.sleep(1)  # Emit one record per second

if __name__ == "__main__":
    for data in generate_sensor_data():
        print(data)
