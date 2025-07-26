FROM python:3.11-slim

# Optimize output and avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install required system dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*
# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port 5000 (for documentation and networking purposes)
EXPOSE 5000

# Start the Flask application
CMD ["python", "run.py"]
