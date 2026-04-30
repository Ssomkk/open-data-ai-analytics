FROM python:3.11-slim

LABEL authors="HP"
LABEL description="Nuclear Safety Analytics — Web Interface"

WORKDIR /app/web

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create static/figures symlink target (figures are served from this folder)
RUN mkdir -p /app/web/static/figures

# Default environment
ENV DATA_DIR=/app/data/raw \
    REPORTS_DIR=/app/reports/lab1 \
    PORT=5000

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

CMD ["python", "app.py"]