
NYC Taxi Trip Data Streaming and Processing

**Project Overview**

This project processes streaming data from NYC taxi trips using Apache Kafka, Apache Spark, FastAPI, and Streamlit. The application ingests data in real-time via Kafka, processes it using Spark, and provides visualizations and APIs for interacting with the processed data.

**Key Components:**
Apache Kafka: Ingests real-time trip data for further processing.
Apache Spark: Processes and parses the real-time data streams.
FastAPI: Provides REST API access to the processed data.
Streamlit: Offers a web-based UI for visualizing the data and metrics.

**Architecture**
Data Ingestion: Kafka ingests the streaming trip data.
Data Processing: Spark reads the data from Kafka and processes it in real-time, parsing the trip details.
Data Visualization: Streamlit displays the processed data in interactive charts and graphs.
API Access: FastAPI serves the processed data through REST endpoints.

**Project Structure**

```
/data
    /checkpoint           # Checkpoints for Spark streaming
    /kafka                # Kafka producer and consumer scripts
    /output               # Output folder for processed data
    /spark                # Spark processing scripts
/docker-compose.yml       # Docker Compose file for orchestrating the containers
/fastapi
    /Dockerfile           # FastAPI Dockerfile
    /app.py               # FastAPI application
/streamlit
    /Dockerfile           # Streamlit Dockerfile
    /app.py               # Streamlit application
/spark-base
    /Dockerfile           # Dockerfile for the Spark base image
    /requirements.txt     # Python dependencies for Spark processing
```

Setup and Running the Project

**Prerequisites**
Ensure the following are installed on your system:

Docker
Docker Compose

**Steps to Run**
1) Clone the repository:

```
git clone https://github.com/rajabhupati/batch-processing-data-system.git
cd batch-processing-data-system
```

2) Build and start the containers: Use Docker Compose to build and start the necessary services:
```docker-compose up --build```

3) Kafka Topic Creation: Make sure the Kafka topic (taxi_trips) is created manually before starting Spark processing:
```
docker exec -it usecase_project-kafka-1 /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic taxi_trips --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
```

4) Send sample data through kafka using following command

 ```  docker exec -it usecase_project-kafka-1  kafka-console-producer.sh --broker-list kafka:9092 --topic taxi_trips```

   Sample data : 

{"trip_id": 1001, "duration": 15, "passenger_count": 2}

{"trip_id": 1004, "duration": 35, "passenger_count": 4}

{"trip_id": 1010, "duration": 50, "passenger_count": 6}



6) Access the services:
Streamlit (for visualization): http://localhost:8501
FastAPI (for REST APIs): http://localhost:8000/docs

**Key Features**

Real-time data ingestion: Streaming NYC taxi trip data using Kafka.
Scalable processing: Spark processes large datasets in real-time.
API access: FastAPI provides a simple interface for querying the processed data.
Visualization: Streamlit offers charts and visualizations for real-time monitoring of the data.


**How It Works**

Data Producer: Kafka producer dynamically generates taxi trip data and pushes it to the taxi_trips topic.
Data Processing: Spark reads the stream from the taxi_trips Kafka topic, parses the data, and writes the processed results to the output folder.
Visualization: Streamlit displays the processed trip data and key metrics on a web-based dashboard.
API: FastAPI exposes endpoints to query the processed trip data.


**Productionizing the Project**

To move this project from a development setup to a production environment, several key changes and improvements need to be implemented. Below are some recommendations for productionizing each component of the system.

**1. Kafka Setup for Production**
Cluster Setup: Instead of running a single Kafka instance, set up a Kafka cluster with multiple brokers for high availability and fault tolerance.
Monitoring: Use tools like Kafka Manager or Confluent Control Center to monitor Kafka brokers, topics, partitions, and consumer groups.
Security: Implement TLS/SSL encryption for communication between brokers and clients. Use SASL authentication for access control to topics and brokers.
Retention Policy: Adjust Kafka’s retention policies based on business requirements for data availability and replayability.


**2. Spark for Production**
Cluster Mode: Run Spark in cluster mode on a distributed cluster like YARN, Kubernetes, or Apache Mesos for improved scalability and fault tolerance.
Checkpointing: Use reliable and distributed storage (e.g., HDFS, S3) for checkpointing instead of local disk.
Error Handling and Fault Tolerance: Add robust error handling and implement retry mechanisms to prevent data loss during streaming.
Resource Management: Use dynamic allocation of executors to scale resources based on load.


**3. FastAPI in Production**
Gunicorn/Uvicorn: Use Gunicorn or Uvicorn with multiple workers to serve the FastAPI application in production.
Load Balancing: Use a reverse proxy like Nginx or HAProxy to distribute incoming traffic and enable SSL termination.
Scaling: Use an orchestrator like Kubernetes or Docker Swarm to scale FastAPI instances horizontally.

**4. Streamlit for Production**
Reverse Proxy: Use Nginx as a reverse proxy to route traffic to the Streamlit app and manage SSL certificates.
Authentication: Implement OAuth or JWT authentication to secure access to the Streamlit dashboard.
Session Management: Use a more robust session state management with a Redis backend for scaling across multiple instances.
Caching: Use Streamlit's built-in caching or external caching like Redis for frequently accessed data.

Apart from this ,Deploying this setup in EKS environment /Docker Swarm and Implementing CI CD, Enhancing security aspects of overall application , Having AIrflow to automate the Spark job scheduling & Importantly adding extensive Logging & Monitoring for these systems could be vital for deploying this app into production



