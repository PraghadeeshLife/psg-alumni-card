FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Set up environment
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Uvicorn
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
