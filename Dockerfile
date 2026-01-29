# Use official Python image for aarch64 (Ubuntu 22.04)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Ubuntu 22.04 aarch64
# espeak-ng for text-to-speech on Linux
RUN apt-get update && apt-get install -y \
    espeak-ng \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ /app/app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
