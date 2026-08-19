# Multi-stage build for Streamlit + Browser Use + Chromium
FROM python:3.12-slim AS base

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y     chromium     chromium-sandbox     fonts-liberation     libnss3     libatk1.0-0     libatk-bridge2.0-0     libcups2     libdrm2     libxkbcommon0     libxcomposite1     libxdamage1     libxrandr2     libgbm1     libpango-1.0-0     libcairo2     libasound2     libxshmfence1     wget     gnupg     && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_FLAGS="--no-sandbox --disable-gpu --disable-dev-shm-usage"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt streamlit

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
