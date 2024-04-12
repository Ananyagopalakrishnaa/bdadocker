# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Install OpenJDK 11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk-headless && \
    apt-get clean;

# Set Java environment variables
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:$PATH

# Create a virtual environment and set it as the default Python environment
RUN python -m venv /opt/venv
ENV PATH /opt/venv/bin:$PATH

# Update pip
RUN pip install --upgrade pip

# Install PySpark
RUN pip install pyspark==3.1.2

# Install spaCy
RUN pip install spacy kafka-python

# Install required packages
RUN pip install cloudpickle

# Create checkpoint directory
RUN mkdir -p /tmp/checkpoint

# Download the spaCy English model
RUN python -m spacy download en_core_web_sm

# Set Spark configurations
ENV PYSPARK_SUBMIT_ARGS="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 pyspark-shell --conf spark.executor.extraJavaOptions=-Dio.netty.tryReflectionSetAccessible=true --conf spark.driver.extraJavaOptions=-Dio.netty.tryReflectionSetAccessible=true"

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Set the default command to run the PySpark script
CMD ["/bin/bash", "-c", "source /opt/venv/bin/activate && python nerscript.py"]
