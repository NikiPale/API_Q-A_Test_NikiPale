FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Waiting for database..."\n\
while ! pg_isready -h db -p 5432 -U $POSTGRES_USER; do\n\
  sleep 1\n\
done\n\
echo "Database is ready!"\n\
echo "Running migrations..."\n\
alembic upgrade head\n\
echo "Starting server..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' > /start.sh && \
chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]