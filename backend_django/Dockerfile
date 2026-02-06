# Production Dockerfile for Django Backend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for SQL Server (ODBC Driver 17)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    gcc \
    g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project files
COPY . .

# Create directory for static and media files
RUN mkdir -p /app/static /app/media

# Expose port
EXPOSE 8000

# Entrypoint script to handle migrations and start Gunicorn
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
