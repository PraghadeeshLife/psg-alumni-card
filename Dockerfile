# Use Python slim image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Playwright dependencies
RUN apt-get update && apt-get install -y wget gnupg curl unzip libnss3 libxss1 libatk-bridge2.0-0 libgtk-3-0

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN pip install --no-cache-dir playwright
RUN playwright install --with-deps chromium

# Copy the app code to the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
