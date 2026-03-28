#!/bin/bash
echo "CONNECT_URL=$CONNECT_URL"
echo "CONNECTOR_NAME=$CONNECTOR_NAME"

echo "Waiting for Kafka Connect at $CONNECT_URL..."
until curl -s "$CONNECT_URL/" | grep -q "version"; do
  echo "Still waiting..."
  sleep 3
done
echo "Kafka Connect is ready"

echo "Checking if connector '$CONNECTOR_NAME' exists..."
if curl -s "$CONNECT_URL/connectors" | grep -q "$CONNECTOR_NAME"; then
  echo "Connector '$CONNECTOR_NAME' already exists. Skipping..."
else
  echo "Creating connector from $CONNECTOR_CONFIG..."
  curl -X POST "$CONNECT_URL/connectors" \
    -H "Content-Type: application/json" \
    -d @"$CONNECTOR_CONFIG"
  echo "Connector creation request sent"
fi

echo "Done!"