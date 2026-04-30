FROM python:3.11-slim

#RUN apt-get update && apt-get install -y --no-install-recommends \
#    gcc \
#    python3-dev \
#    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/data_quality_analysis

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/raw

CMD ["python", "app.py"]