# ---------- 1. Базовий образ ----------
FROM python:3.12-slim AS base

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Робоча директорія — батьківська для пакета
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Залежності (кешований шар)
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Код копіюється як пакет auth_service/
COPY . ./auth_service/

EXPOSE 8000

# Запуск з вказанням пакета — відносні імпорти працюють
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]



