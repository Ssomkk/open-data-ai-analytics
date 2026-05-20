FROM python:3.11-slim

WORKDIR /app/visualization

#RUN apt-get update && apt-get install -y \
#    gcc \
#    g++ \
#    libfreetype6-dev \
#    libpng-dev \
#    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/raw /app/visualization/reports/lab1/figures

CMD ["python", "app.py"]