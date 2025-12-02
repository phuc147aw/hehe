import os
import requests
import base64
import time
import librosa
from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, emit
from loguru import logger

from infer import VietASR

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
socketio = SocketIO(app, cors_allowed_origins="*")

# Model paths
config = 'configs/quartznet12x1_vi.yaml'
encoder_checkpoint = 'models/acoustic_model/vietnamese/Encoder-STEP-289936.pt'
decoder_checkpoint = 'models/acoustic_model/vietnamese/Decoder-STEP-289936.pt'
lm_path = 'models/language_model/5-gram-lm.binary'

# Load ASR model
vietasr = VietASR(
    config_file=config,
    encoder_checkpoint=encoder_checkpoint,
    decoder_checkpoint=decoder_checkpoint,
    lm_path=lm_path,
    beam_width=50
)

STATIC_DIR = "static"
UPLOAD_DIR = "upload"
RECORD_DIR = "record"

os.makedirs(os.path.join(STATIC_DIR, UPLOAD_DIR), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, RECORD_DIR), exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html", audio_path=None)

@socketio.on('connect')
def connected():
    logger.info("CONNECTED: " + request.sid)
    emit('to_client', {'text': request.sid})

@socketio.on('to_server')
def response_to_client(data):
    logger.info(data["text"])
    emit('to_client', {'text': len(data["text"].split())})

@socketio.on('audio_to_server')
def handle_audio_from_client(data):
    filename = time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(STATIC_DIR, RECORD_DIR, filename + ".wav")

    with open(filepath, "wb") as audio_file:
        decode_string = base64.b64decode(data["audio_base64"].split(",")[1])
        audio_file.write(decode_string)

    logger.info("ASR processing...")
    audio_signal, _ = librosa.load(filepath, sr=16000)
    transcript = vietasr.transcribe(audio_signal)

    emit('audio_to_client', {'filepath': filepath, 'transcript': transcript})

@app.route('/upload', methods=['POST'])
def handle_upload():
    _file = request.files.get('file')
    if not _file or _file.filename == "":
        return redirect("/")

    filepath = os.path.join(STATIC_DIR, UPLOAD_DIR, _file.filename)
    _file.save(filepath)

    audio_signal, _ = librosa.load(filepath, sr=16000)
    transcript = vietasr.transcribe(audio_signal)

    return render_template("index.html", transcript=transcript, audiopath=filepath)

# Quan trọng: KHÔNG chạy socketio.run khi deploy
# Render sẽ chạy qua gunicorn
