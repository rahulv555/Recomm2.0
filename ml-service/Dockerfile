FROM python:3.12-slim

WORKDIR /app

# System deps needed for psycopg2 / some ML libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch==2.5.1+cu121 --index-url https://download.pytorch.org/whl/cu121
# Copy the app code
COPY . .    

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python -m app.init_redis && uvicorn app.main:app --host 0.0.0.0 --port 8088 --workers 4"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8088", "--workers", "4"]

# ../.venv/Scripts/uvicorn app.main:app --host 0.0.0.0 --port 8088 --workers 4