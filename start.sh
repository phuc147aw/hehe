#!/usr/bin/env bash
set -e
./download_models.sh || true

echo "Preflight import check..."
python scripts/check_imports.py || true

if [ "$PRELOAD_MODEL" = "1" ]; then
  echo "Preloading model..."
  python - <<PY
from app import get_vietasr
get_vietasr()
print("Model preloaded")
PY
fi

exec gunicorn -k eventlet -w 1 app:app -b 0.0.0.0:${PORT:-8080}
