FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/starwars_pages /app/chroma_db

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DATA_PATH=/app/data
ENV STARWARS_PAGES_PATH=/app/data/starwars_pages

CMD ["python", "simple_rag.py"]