# 🚀 EventFlow: Real-Time CDC Notification Pipeline

A production-style **Change Data Capture (CDC)** pipeline that captures database changes and triggers real-time notifications using **Debezium + Apache Kafka**.

---

## 🧠 Overview

EventFlow demonstrates how to build an **event-driven system** where database changes automatically trigger downstream actions.

Whenever a new user is created in PostgreSQL, the system:
1. Captures the change using CDC
2. Streams it through Kafka
3. Processes the event in a consumer service
4. Sends a notification email

---

## 🏗️ Architecture

```
INSERT INTO users
↓
Debezium captures change (WAL)
↓
Kafka topic: cdc.public.users
↓
Consumer processes event (op = "c")
↓
Email sent to user
```
## 🧩 Key Features

- Real-time **CDC pipeline using Debezium**
- Event-driven architecture using **Apache Kafka**
- Schema-aware event handling (Debezium envelope parsing)
- Operation-based filtering (`INSERT`, `UPDATE`, `DELETE`)
- Automatic **Kafka topic readiness detection**
- Fault-tolerant consumer with logging and validation
- Containerized setup using Docker Compose

---

## ⚙️ Setup Instructions

### Generate Kafka Cluster ID

```bash
# Kafka in KRaft mode requires a CLUSTER_ID that must be explicitly set
docker run --rm confluentinc/cp-kafka:7.5.0 kafka-storage random-uuid

# Add this inside Kafka environment in docker-compose.yml
CLUSTER_ID: "your-generated-id"
```

### Build and Run

```bash
docker-compose down -v \
  && docker volume prune -f \
  && docker rmi cdc-pipeline-notification \
  && docker-compose up --build -d
```

## Verification Steps

### 1. Insert Data into PostgreSQL

```bash
docker exec -it cdc-pipeline-postgres psql -U postgres -d inventory
```

```sql
INSERT INTO users (name, email) VALUES ('Abhinav', 'abhinav@test.com');
SELECT * FROM users;
```

### 2. Verify Kafka Topic Creation

```bash
docker exec -it cdc-pipeline-kafka kafka-topics \
  --list \
  --bootstrap-server kafka:9092
```

#### Expected topics:
```bash
cdc.public.orders
cdc.public.users
```
### 3. Check Consumer Logs

```bash
docker logs -f cdc-pipeline-notification
```

#### Expected output:
```bash
2026-03-28 15:32:25,296 - INFO - Topic cdc.public.users is ready
2026-03-28 15:32:25,305 - INFO - Starting Kafka consumer...
2026-03-28 15:32:25,306 - INFO - Subscribed to topic: cdc.public.users
```

### 4. Verify Connector

```bash
curl http://localhost:8083/connectors
curl http://localhost:8083/connectors/postgres-connector/status
```

#### Expected Output
```bash
["postgres-connector"] #first call

{"name":"postgres-connector","connector":{"state":"RUNNING","worker_id":"172.19.0.5:8083"},"tasks":[{"id":0,"state":"RUNNING","worker_id":"172.19.0.5:8083"}],"type":"source"}
```

#### Register Debezium Connector (manually)

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @connectors/postgres-connector.json
```

### 5. Verify Email (Maildev)

```bash
http://localhost:1080
```