FROM python:3.10-slim

# Install curl and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium
RUN apt-get update && apt-get install -y chromium

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set environment variables for Chromium and ChromeDriver
ENV PATH="/usr/local/bin/:$PATH"
ENV CHROME_BIN="/usr/bin/chromium"

# Set up the Python environment
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Uvicorn
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
