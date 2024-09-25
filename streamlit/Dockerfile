FROM python:3.9-slim

# Install OpenJDK 17 for PySpark
RUN apt-get update && apt-get install -y openjdk-17-jre-headless && apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["streamlit", "run", "app.py"]
