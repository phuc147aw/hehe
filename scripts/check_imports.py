modules = [
    # Web / runtime
    "flask", "flask_socketio", "eventlet", "gunicorn",

    # Audio / numeric
    "librosa", "numpy", "soundfile", "audioread", "loguru",

    # NeMo core
    "nemo_toolkit",  # thực tế import là 'nemo', nhưng check tên gói
    "nemo", "hydra", "omegaconf", "pytorch_lightning",

    # Hugging Face
    "huggingface_hub", "transformers", "tokenizers", "safetensors",

    # NeMo ASR phụ trợ
    "braceexpand", "webdataset", "pandas", "sentencepiece",
    "ruamel.yaml", "ruamel.yaml.clib", "pyctcdecode", "soxr", "sox",
    "tensorboard", "youtokentome",
]

def try_import(name):
    real_name = name
    # Map một số tên gói sang tên import thực
    mapping = {
        "flask_socketio": "flask_socketio",
        "pytorch_lightning": "pytorch_lightning",
        "huggingface_hub": "huggingface_hub",
        "ruamel.yaml": "ruamel.yaml",
        "ruamel.yaml.clib": "ruamel.yaml.clib",
        "nemo_toolkit": "nemo",  # gói 'nemo-toolkit' import là 'nemo'
    }
    real_name = mapping.get(name, name)
    try:
        __import__(real_name)
        print(f"OK: {name}")
    except Exception as e:
        print(f"MISS: {name} -> {type(e).__name__}: {e}")

if __name__ == "__main__":
    for m in modules:
        try_import(m)
