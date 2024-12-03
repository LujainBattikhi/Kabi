# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    wget \
    curl \
    gnupg \
    && apt-get clean

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