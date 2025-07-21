# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but recommended for some PyPi packages)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Expose a port if needed (for Flask or other services)
# EXPOSE 8080

# Run the bot
CMD ["python", "main.py"]
