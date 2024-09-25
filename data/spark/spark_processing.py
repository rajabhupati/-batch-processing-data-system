from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the schema for the incoming data
schema = StructType([
    StructField("trip_id", IntegerType(), True),
    StructField("duration", IntegerType(), True),
    StructField("passenger_count", IntegerType(), True)
])

# Initialize Spark Session
try:
    spark = SparkSession.builder \
        .appName("NYC Taxi Trip Processor - Streaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,org.apache.kafka:kafka-clients:3.5.2") \
        .getOrCreate()
    logger.info("Spark session created successfully.")
except Exception as e:
    logger.error(f"Error creating Spark session: {e}")
    raise

# Read from Kafka topic
try:
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "taxi_trips") \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()
    logger.info("Successfully connected to Kafka and subscribed to the topic 'taxi_trips'.")
except Exception as e:
    logger.error(f"Error connecting to Kafka: {e}")
    raise

# Parse the Kafka data (which is in JSON)
try:
    parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    logger.info("Data parsing successful.")
except Exception as e:
    logger.error(f"Error parsing data from Kafka: {e}")
    raise

# Write the parsed data to JSON (no aggregation, just forwarding parsed data)
try:
    query = parsed_df.writeStream \
        .outputMode("append") \
        .format("json") \
        .option("checkpointLocation", "/data/checkpoint/") \
        .option("path", "/data/output/processed_trips/") \
        .start()
    logger.info("Streaming query started successfully.")
except Exception as e:
    logger.error(f"Error starting streaming query: {e}")
    raise

# Wait for the streaming to finish
try:
    query.awaitTermination()
except Exception as e:
    logger.error(f"Error during streaming query execution: {e}")
    raise
