FROM python:3.7-slim as development

ENV PYTHONUNBUFFERED=1
WORKDIR /app/backend

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

