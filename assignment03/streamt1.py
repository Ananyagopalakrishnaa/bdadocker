import time
import json
import os
import logging
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaTimeoutError
from newsapi import NewsApiClient

logging.basicConfig(level=logging.INFO)

# Set News API key
os.environ['NEWS_API_KEY'] = '670c36ccfaac4136836b803f727940f3'  # Keep the API key in the script for now

# Initialize News API client
newsapi = NewsApiClient(api_key=os.environ['NEWS_API_KEY'])

# Retry mechanism for Kafka connection
def connect_kafka_producer():
    retries = 0
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9093',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=600  # Increase timeout to 100 seconds
            )
            logging.info("Successfully connected to Kafka")
            return producer
        except NoBrokersAvailable as e:
            retries += 1
            logging.error(f"Failed to connect to Kafka, retrying ({retries}/10)...")
            if retries > 10:
                raise e
            time.sleep(5)
        except KafkaTimeoutError as e:
            logging.error(f"KafkaTimeoutError: {e}")
            raise e
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise e

try:
    producer = connect_kafka_producer()

    def fetch_news():
        # Fetch real-time news
        top_headlines = newsapi.get_top_headlines(language='en', country='us')
        articles = top_headlines['articles']
        return articles

    if __name__ == "__main__":
        iteration = 0
        while True:
            iteration += 1
            articles = fetch_news()

            # Print headlines and news content with iteration count
            for article in articles:
                logging.info(f"Iteration {iteration}: Headline: {article['title']}")
                logging.info(f"News: {article['description']}")
                logging.info("-" * 50)

            # Write articles to Kafka topic
            for article in articles:
                producer.send('topic1', value={"headline": article['title'], "news": article['description']})

            logging.info(f"Iteration {iteration}: Fetched and sent {len(articles)} articles to Kafka topic1")

            # Sleep for 15 seconds before fetching again
            time.sleep(15)

except KeyboardInterrupt:
    logging.info("Script interrupted. Exiting...")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    if producer:
        producer.flush()
        producer.close()
