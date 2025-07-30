FROM python:3.14.0rc1-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Expose a port if needed (for Flask or other services)
# EXPOSE 8080

# Run the bot
CMD ["python", "main.py"]
