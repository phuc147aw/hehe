FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    swig \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install CPU PyTorch wheel first
RUN pip install --no-cache-dir torch==1.13.1+cpu torchaudio==0.13.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Copy requirements and install dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .

# Set execute permissions for scripts
RUN chmod +x download_models.sh start.sh

# Expose port
EXPOSE 8080

# Run the application
CMD ["./start.sh"]
