FROM python:3.12 AS builder
WORKDIR /build
COPY ./requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /install /usr/local

COPY . /app/auth_service/

ENV PYTHONPATH=/app

USER 1000
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
