FROM bitnami/spark:latest

# Install kafka-python for KafkaProducer
COPY requirements.txt .


RUN pip install --no-cache-dir --force-reinstall kafka-python==2.0.2 six==1.16.0

