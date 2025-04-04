import time
import random
from faker import Faker

fake = Faker()

def generate_sensor_data():
    while True:
        data = {
            "timestamp": int(time.time()),
            "sensor_id": fake.uuid4(),
            "temperature": round(random.uniform(20.0, 100.0), 2),  # °C, rounding to 2 decimal places
            "pressure": round(random.uniform(1.0, 10.0), 2),      # bar, rounding to 2 decimal places
            "flow_rate": round(random.uniform(0.5, 5.0), 2),       # m³/s, rounding to 2 decimal places
            "status": random.choice(["NORMAL", "WARNING", "ALARM"]) # Randomly choose status
        }
        yield data
        time.sleep(1)  # Emit data every 1 second

if __name__ == "__main__":
    for data in generate_sensor_data():
        print(data)
