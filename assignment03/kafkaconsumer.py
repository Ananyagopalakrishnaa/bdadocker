import logging
import threading
from kafka import KafkaConsumer

# Initialize logging
logging.basicConfig(level=logging.INFO)

def consume_messages():
    # Kafka consumer to read messages from topic2
    consumer = KafkaConsumer(
        'topic2',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group1',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    for message in consumer:
        logging.info(f"Key: {message.key.decode()}, Value: {message.value}")

if __name__ == "__main__":
    # Create and start the consumer thread
    logging.info("Starting Kafka consumer...")
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    # Wait for the thread to finish
    consumer_thread.join()
