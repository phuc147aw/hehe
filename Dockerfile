# Dockerfile cho demo trên Render (CPU)
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps cho audio / build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsndfile1 \
    swig \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements-prod.txt /app/requirements.txt

RUN pip install --upgrade pip

# Cài torch CPU wheel trước (chọn CPU wheel để tránh cần CUDA trên Render)
RUN pip install --no-cache-dir torch==1.13.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Cài các package runtime (bao gồm NeMo - có thể nặng)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app code & scripts
COPY . /app
RUN chmod +x /app/download_models.sh /app/start.sh

EXPOSE 8080

CMD ["./start.sh"]
