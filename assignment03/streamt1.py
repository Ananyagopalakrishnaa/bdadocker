import time
import json
import logging
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaTimeoutError
from newsapi import NewsApiClient

logging.basicConfig(level=logging.INFO)

# Set News API key directly
NEWS_API_KEY = '670c36ccfaac4136836b803f727940f3'

# Initialize News API client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def connect_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=600
            )
            logging.info("Successfully connected to Kafka")  
            return producer
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(5)

def fetch_news():
    top_headlines = newsapi.get_top_headlines(language='en', country='us')
    articles = top_headlines['articles']
    return articles

if __name__ == "__main__":
    time.sleep(10)  # Delay for 10 seconds to let Kafka initialize fully

    producer = connect_kafka_producer()
    
    iteration = 0
    while True:
        iteration += 1
        articles = fetch_news()

        for article in articles:
            logging.info(f"Iteration {iteration}: Headline: {article['title']}")  
            logging.info(f"News: {article['description']}")  
            logging.info("-" * 50)  

        for article in articles:
            producer.send('streamtopic1', value={"headline": article['title'], "news": article['description']})

        logging.info(f"Iteration {iteration}: Fetched and sent {len(articles)} articles to Kafka streamtopic1")  
        
        time.sleep(60)
