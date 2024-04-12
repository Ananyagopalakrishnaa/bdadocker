# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Install necessary tools and dependencies
RUN apt-get update && \
    apt-get install -y wget iputils-ping && \
    apt-get clean

# Set working directory
WORKDIR /opt/kafka

# Download and extract Kafka binaries
RUN wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz && \
    tar -xzf kafka_2.13-3.7.0.tgz && \
    mv kafka_2.13-3.7.0/* . && \
    rm kafka_2.13-3.7.0.tgz && \
    rmdir kafka_2.13-3.7.0

# Set the working directory in the container
WORKDIR /app

# Create a virtual environment and set it as the working directory
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies inside the virtual environment
RUN pip install --upgrade pip
RUN pip install kafka-python newsapi-python

# Copy the Python script into the container
COPY streamt1.py /app/

# Run the Python script
CMD ["python", "streamt1.py"]
