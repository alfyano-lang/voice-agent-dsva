# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (needed for some python packages or audio tools)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose ports if necessary (ARI usually connects OUT to Asterisk, but if we have a web hook, we might need EXPOSE)
# For this agent, it acts as a client to ARI, so no inbound ports strictly needed unless we add a web interface.

# Define environment variable defaults
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "ari_app.py"]
