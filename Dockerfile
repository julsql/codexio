FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /app/bd/database /app/bd/media && \
    chmod -R 755 /app/bd/media && \
    chown -R www-data:www-data /app/bd/media/ && \
    python3 bd/manage.py migrate

EXPOSE 8000

CMD ["python", "bd/manage.py", "runserver", "0.0.0.0:8000"]