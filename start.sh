#!/usr/bin/env bash
set -e

# Download models if URLs provided
./download_models.sh || true

# Optionally preload model to avoid first-request latency:
if [ "$PRELOAD_MODEL" = "1" ]; then
  echo "Preloading model..."
  python - <<PY
from app import get_vietasr
get_vietasr()
print("Model preloaded")
PY
fi

# Run gunicorn with eventlet worker for Flask-SocketIO
exec gunicorn -k eventlet -w 1 app:app -b 0.0.0.0:${PORT:-8080}