# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies for numpy/pandas
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory
COPY src/ ./src/

# Copy the CSV data file to src directory (where datahandler expects it)
COPY src/complete_player_stats10.csv ./src/

# Add src to Python path
ENV PYTHONPATH=/app/src

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application - note we're now in /app and importing from src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]