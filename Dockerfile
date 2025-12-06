FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsndfile1 \
    swig \
    git \
    wget \
    cmake \
    libbz2-dev \
    liblzma-dev \
    pkg-config \
    sox \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip --root-user-action=ignore

# Torch CPU wheel
RUN pip install --no-cache-dir torch==1.13.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html --root-user-action=ignore

# Install remaining deps
RUN pip install --no-cache-dir -r /app/requirements.txt --root-user-action=ignore

# Force pins nhạy cảm để đảm bảo tương thích NeMo
RUN pip install --no-cache-dir --force-reinstall --no-deps huggingface-hub==0.14.1 --root-user-action=ignore
RUN pip install --no-cache-dir --force-reinstall --no-deps braceexpand==0.1.7 --root-user-action=ignore

# App files
COPY . /app
RUN chmod +x /app/download_models.sh /app/start.sh

EXPOSE 8080
CMD ["./start.sh"]
