import logging
import spacy
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, explode, col, udf, to_json
from pyspark.sql.types import StringType, StructType, StructField, ArrayType

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

spark = SparkSession.builder \
    .appName("NERStreamProcessor") \
    .config("spark.streaming.uninterruptible", "true") \
    .getOrCreate()

# Define the schema for the incoming Kafka messages
schema = StructType([
    StructField("headline", StringType()),
    StructField("news", StringType())
])

# Function to perform NER using spaCy
def perform_ner_spacy(text):
    if text is None:
        return []
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.text.strip()]
    return entities

# Define the udf
perform_ner_udf = udf(perform_ner_spacy, ArrayType(StringType()))

# Read from Kafka streamtopic1
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "streamtopic1") \
    .load()

# Convert value column to string and then parse JSON
df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Perform NER and explode the entities
df_ner = df_parsed.withColumn("entities", explode(perform_ner_udf(col("news")))) \
    .filter(col("entities") != "") \
    .groupBy("entities") \
    .count() \
    .selectExpr("to_json(struct(*)) AS value")

# Write the named entities count to Kafka topic2
query = df_ner \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "topic2") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .outputMode("update") \
    .start()

query.awaitTermination()
