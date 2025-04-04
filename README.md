# ‚ö° Real-Time SCADA Data Pipeline with Kafka and PostgreSQL

This project simulates a real-time data pipeline where a fake SCADA system streams sensor data every second. The architecture includes Kafka for real-time data streaming and PostgreSQL for persistent storage.

## Ì≥å Architecture Overview

\`\`\`
[Fake SCADA System] --> [Kafka Producer] --> [Kafka Topic] --> [Kafka Consumer] --> [PostgreSQL Database]
\`\`\`

### Components:

- **Fake SCADA System**: Simulates real sensors by generating random readings every second.
- **Kafka Producer**: Acts on behalf of the SCADA system and sends the data to a Kafka topic.
- **Kafka Broker**: Handles message streaming between producers and consumers.
- **Kafka Consumer**: Subscribes to the topic and inserts the received data into a PostgreSQL table.
- **PostgreSQL**: Stores the time-series sensor data persistently for querying and analytics.

---

## Ì¥ß Setup Instructions

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/yourusername/scada-kafka-dashboard.git
cd scada-kafka-dashboard
\`\`\`

### 2. Create a Virtual Environment and Install Dependencies

\`\`\`bash
python3 -m venv scada_venv
source scada_venv/bin/activate
pip install -r requirements.txt
\`\`\`

---

### 3. Install and Start Kafka (Using Docker)

Create a \`docker-compose.yml\` file:

\`\`\`yaml
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
\`\`\`

Then run:

\`\`\`bash
docker-compose up -d
\`\`\`

---

### 4. Create Kafka Topic

\`\`\`bash
docker exec -it <kafka_container_id_or_name> bash
kafka-topics --create --topic scada-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
\`\`\`

---

### 5. Set Up PostgreSQL

\`\`\`bash
sudo -u postgres psql
\`\`\`

\`\`\`sql
CREATE USER scada_user WITH PASSWORD 'scada_pass';
CREATE DATABASE scada_db OWNER scada_user;
GRANT ALL PRIVILEGES ON DATABASE scada_db TO scada_user;
\`\`\`

---

### 6. Create the \`sensor_data\` Table (Automatically via Consumer)

The table will be auto-created by the consumer script if not already present:

\`\`\`sql
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    sensor_id UUID,
    temperature FLOAT,
    pressure FLOAT,
    flow_rate FLOAT,
    status VARCHAR(50)
);
\`\`\`

---

## Ì∫Ä Running the Project

### Start Kafka Producer (Fake SCADA System)

\`\`\`bash
python producer.py
\`\`\`

### Start Kafka Consumer

\`\`\`bash
python consumer.py
\`\`\`

---

## Ì≥ä Query the Data in PostgreSQL

\`\`\`bash
psql -U postgres -d scada_db
\`\`\`

Then:

\`\`\`sql
SELECT COUNT(*) FROM sensor_data;
SELECT * FROM sensor_data ORDER BY id DESC LIMIT 5;
\`\`\`

---

## ‚úÖ Real SCADA System Integration

For a real SCADA system:
- Replace the fake \`producer.py\` script.
- Use a real Kafka producer that reads data from hardware or SCADA interface (e.g., OPC UA, MQTT, REST, Modbus).
- Keep Kafka and PostgreSQL pipeline as-is.

---

## Ì≥Å Project Structure

\`\`\`
‚îú‚îÄ‚îÄ producer.py         # Simulates SCADA sensor data and sends to Kafka
‚îú‚îÄ‚îÄ consumer.py         # Reads from Kafka and inserts into PostgreSQL
‚îú‚îÄ‚îÄ requirements.txt    # Python dependencies
‚îú‚îÄ‚îÄ docker-compose.yml  # Kafka + Zookeeper setup
‚îú‚îÄ‚îÄ .env                # DB connection details (optional)
‚îî‚îÄ‚îÄ README.md
\`\`\`

---

## Ì∑™ Sample Output

\`\`\`sql
SELECT * FROM sensor_data ORDER BY id DESC LIMIT 5;
\`\`\`

| id   | timestamp           | sensor_id                            | temperature | pressure | flow_rate | status  |
|------|---------------------|---------------------------------------|-------------|----------|-----------|---------|
| 3832 | 2025-04-04 19:15:53 | 2087ca10-d69e-443c-98fc-124c215f4973 | 38.17       | 8.84     | 2.62      | WARNING |
| 3831 | 2025-04-04 19:15:52 | b0e5bf6b-66a1-4976-997b-2bde6dc64d68 | 87.16       | 8.33     | 3.17      | NORMAL  |

---

## Ì≥¨ Contact

For questions or feedback, feel free to reach out or contribute!
