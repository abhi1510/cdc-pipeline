import json
import logging
import os
import smtplib
import time
from email.mime.text import MIMEText

from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
FROM_EMAIL = os.getenv("FROM_EMAIL")
SUBJECT = "Welcome Onboard"

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("TOPIC")
GROUP_ID = os.getenv("GROUP_ID")


def wait_for_topic():
    admin = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    while True:
        topics = admin.list_topics(timeout=5).topics
        if TOPIC in topics:
            logger.info(f"Topic {TOPIC} is ready")
            return
        logger.info(f"Waiting for topic {TOPIC} on {KAFKA_BOOTSTRAP_SERVERS}")
        time.sleep(3)


def send_email(to_email, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = SUBJECT
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)

        logger.info(f"Email sent to {to_email}")

    except Exception as e:
        logger.error(f"Failed to send email: {e}", exc_info=True)


consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "security.protocol": "PLAINTEXT",
    }
)


def main():

    logger.info("Starting Kafka consumer...")
    consumer.subscribe([TOPIC])
    logger.info(f"Subscribed to topic: {TOPIC}")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            # Deserialize message
            msg_value = msg.value()
            if msg_value is None:
                continue

            payload = json.loads(msg_value.decode("utf-8"))
            logger.info(f"Received message: {payload}")

            # Handle Debezium envelope
            data = payload.get("payload", payload)

            # Only process CREATE events
            if data.get("op") != "c":
                continue

            after = data.get("after")
            if not after:
                logger.warning("No 'after' field found, skipping...")
                continue

            email = after.get("email")
            name = after.get("name")

            if not email:
                logger.warning("Email not found, skipping...")
                continue

            body = f"Hi {name}, your account has been created."

            send_email(email, body)

            logger.info(f"Notification sent | name={name}, email={email}")

    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        consumer.close()
        logger.info("Consumer closed")


if __name__ == "__main__":
    wait_for_topic()
    main()
