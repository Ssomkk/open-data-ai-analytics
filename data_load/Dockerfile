FROM python:3.11-slim

WORKDIR /app/data_load

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/raw

CMD ["python", "app.py"]