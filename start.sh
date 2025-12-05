#!/usr/bin/env bash
set -e
./download_models.sh || true

echo "Debug: checking installed packages..."
python - <<PY
import importlib, pkgutil
print("braceexpand found:", pkgutil.find_loader("braceexpand") is not None)
import huggingface_hub
print("huggingface_hub version:", getattr(huggingface_hub, "__version__", "unknown"))
PY

if [ "$PRELOAD_MODEL" = "1" ]; then
  echo "Preloading model..."
  python - <<PY
from app import get_vietasr
get_vietasr()
print("Model preloaded")
PY
fi

exec gunicorn -k eventlet -w 1 app:app -b 0.0.0.0:${PORT:-8080}
