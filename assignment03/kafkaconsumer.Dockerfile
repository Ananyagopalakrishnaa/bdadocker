# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Create a virtual environment and set it as the default Python environment
RUN python -m venv /opt/venv
ENV PATH /opt/venv/bin:$PATH

# Update pip
RUN pip install --upgrade pip

# Install Kafka consumer library
RUN pip install kafka-python

# Set working directory
WORKDIR /app

# Copy the Kafka consumer script into the container
COPY kafkaconsumer.py /app/

# Set the default command to run the Kafka consumer
CMD ["/bin/bash", "-c", "source /opt/venv/bin/activate && python kafkaconsumer.py"]
