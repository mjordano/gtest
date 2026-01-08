# Backend Dockerfile
FROM python:3.11-slim

# Postavljanje radnog direktorijuma
WORKDIR /app

# Instaliranje sistemskih zavisnosti
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiranje requirements i instaliranje Python zavisnosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiranje aplikacije
COPY . .

# Postavljanje environment varijabli
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Pokretanje aplikacije
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
