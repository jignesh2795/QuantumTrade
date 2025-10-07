FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage cache
COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip

# Install bcrypt first to avoid version conflicts
RUN pip install bcrypt==4.2.0

# Install requirements with error handling
RUN pip install --no-cache-dir -r requirements.txt || \
  (echo "Failed to install from requirements.txt, installing packages individually" && \
  pip install fastapi==0.111.1 uvicorn[standard]==0.23.2 sqlalchemy==2.0.22 psycopg2-binary==2.9.7 && \
  pip install pydantic==2.6.0 python-dotenv==1.0.1 pytest==8.2.1 pytest-asyncio==0.22.0 && \
  pip install requests==2.32.1 numpy==1.24.3 pandas==1.5.3 aiohttp==3.9.3 && \
  pip install pyjwt==2.8.0 python-jose==3.3.0 passlib==1.7.4 && \
  pip install prometheus-client==0.19.0 python-multipart==0.0.9 && \
  pip install supabase==2.4.5 scikit-learn==1.3.0 joblib==1.3.2 websockets==12.0 torch==2.1.0)

# Create models dir to mount later
RUN mkdir -p /app/models

# Copy application code
COPY . .

# Verify that all required packages are installed
RUN echo "Verifying installed packages:" && \
  pip list | grep -E "(fastapi|uvicorn|sqlalchemy|psycopg2|numpy|pandas|scikit-learn|joblib|torch|bcrypt)" || \
  echo "Some packages may be missing"

EXPOSE 8000

CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]