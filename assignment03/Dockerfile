FROM python:3.9-slim

# Install ping utility
RUN apt-get update && \
    apt-get install -y iputils-ping && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY streamt1.py /app/

# Install required Python packages
RUN pip install kafka-python newsapi-python

# Run the Python script
CMD ["python", "streamt1.py"]
