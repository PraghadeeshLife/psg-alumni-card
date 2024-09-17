# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    libxtst6 \
    libgtk-3-0 \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libxt6 \
    libpci-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Firefox
RUN wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US" \
    && tar xjf firefox.tar.bz2 -C /opt/ \
    && ln -s /opt/firefox/firefox /usr/bin/firefox \
    && rm firefox.tar.bz2

# Install geckodriver
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
    && tar -xzf geckodriver.tar.gz -C /usr/local/bin \
    && rm geckodriver.tar.gz \
    && chmod +x /usr/local/bin/geckodriver

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]