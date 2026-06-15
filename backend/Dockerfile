FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY CSGO.csv /data/CSGO.csv

# Entrenar modelo en build (no bloquea el arranque en Render)
RUN python -m scripts.train_model \
    --csv-path /data/CSGO.csv \
    --output app/ml/models/kmeans_pca_model.joblib

ENTRYPOINT ["python", "-m", "scripts.docker_entrypoint"]
