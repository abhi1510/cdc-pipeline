# cdc-pipeline
A real-time Change Data Capture (CDC) pipeline built using Debezium and Apache Kafka.  
This project demonstrates how to capture database changes and process them into meaningful business events in a scalable, event-driven architecture.

---

## 🧠 Overview

EventFlow captures changes from a PostgreSQL database using Debezium and streams them through Kafka for real-time processing.

It transforms low-level CDC events into clean, domain-specific events that can be consumed by downstream services like analytics, notifications, or anomaly detection systems.

---

## 🏗️ Architecture

PostgreSQL → Debezium → Kafka → Processor Service → Consumers

- **PostgreSQL**: Source database (WAL-based CDC)
- **Debezium**: Captures database changes
- **Kafka**: Event streaming platform
- **Processor Service**: Transforms raw CDC events into business events
- **Consumers**: Downstream services (analytics, notifications, etc.)

---

## 🔧 Tech Stack

- Python / Golang (for services)
- Apache Kafka
- Debezium
- PostgreSQL
- Docker & Docker Compose


---

## ⚙️ Setup Instructions

### 1. Start Infrastructure

```bash
docker-compose up -d
```

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT,
  amount INT
);
```

```bash
curl -X POST http://localhost:8083/connectors \
-H "Content-Type: application/json" \
-d @connectors/postgres-connector.json
```

```sql
INSERT INTO users (name, email) VALUES ('Abhinav', 'abhinav@test.com');
```
