#!/bin/bash
# Entrypoint script for Render deployment
# Downloads models and starts gunicorn with eventlet worker

set -e

echo "=== Starting application ==="

# Download models
./download_models.sh

# Optionally preload model
if [ "$PRELOAD_MODEL" = "1" ]; then
    echo "Preloading model..."
    python -c "from app import get_vietasr; get_vietasr()"
    echo "Model preloaded."
fi

# Start gunicorn with eventlet worker
echo "Starting gunicorn..."
exec gunicorn -k eventlet -w 1 app:app -b 0.0.0.0:${PORT:-8080}
