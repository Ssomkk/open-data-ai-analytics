FROM python:3.11-slim

#RUN apt-get update && apt-get install -y --no-install-recommends \
#    libpng-dev \
#    libfreetype6-dev \
#    && rm -rf /var/lib/apt/lists/* \

#RUN apt-get update && apt-get install -y \
#    gcc \
#    g++ \
#    libpq-dev \
#    libfreetype6-dev \
#    libpng-dev \
#    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/data_research

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/raw /app/data_research/reports/lab1/figures

CMD ["python", "app.py"]
