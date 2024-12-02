# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the project files
COPY . .

# Copy the entrypoint script from devops directory
COPY devops/entry /app/devops/entry

# Make the script executable
RUN chmod +x /app/devops/entry

# Set the entrypoint
ENTRYPOINT ["/app/devops/entry"]