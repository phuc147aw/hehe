#!/usr/bin/env python3
import os
import base64
import time
import librosa
from flask import Flask, redirect, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from loguru import logger

# NOTE: không import VietASR ở cấp module để tránh import nặng khi model chưa có
vietasr = None

def get_vietasr():
    global vietasr
    if vietasr is None:
        # load model paths từ env (nếu không set thì dùng mặc định trong repo)
        config = os.environ.get('ASR_CONFIG', 'configs/quartznet12x1_vi.yaml')
        encoder_checkpoint = os.environ.get('ENCODER_CHECKPOINT', 'models/acoustic_model/vietnamese/Encoder-STEP-289936.pt')
        decoder_checkpoint = os.environ.get('DECODER_CHECKPOINT', 'models/acoustic_model/vietnamese/Decoder-STEP-289936.pt')
        lm_path = os.environ.get('LM_PATH', 'models/language_model/5-gram-lm.binary')
        beam_width = int(os.environ.get('BEAM_WIDTH', '50'))

        # Import nặng bên trong hàm — chỉ khi cần khởi tạo model
        from infer import VietASR
        logger.info("Initializing VietASR...")
        vietasr = VietASR(
            config_file=config,
            encoder_checkpoint=encoder_checkpoint,
            decoder_checkpoint=decoder_checkpoint,
            lm_path=lm_path,
            beam_width=beam_width
        )
        logger.info("VietASR loaded")
    return vietasr

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret-key")
socketio = SocketIO(app, cors_allowed_origins="*")

STATIC_DIR = "static"
UPLOAD_DIR = "upload"
RECORD_DIR = "record"

os.makedirs(os.path.join(STATIC_DIR, UPLOAD_DIR), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, RECORD_DIR), exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html", audio_path=None)

@app.route("/health")
def health():
    # readiness: nếu model đã loaded trả 200, nếu chưa trả 503 để Render biết đang khởi động
    if vietasr is not None:
        return jsonify({"status":"ok","model_loaded":True}), 200
    else:
        return jsonify({"status":"starting","model_loaded":False}), 503

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

    # đảm bảo model đã được load
    model = get_vietasr()
    transcript = model.transcribe(audio_signal)

    emit('audio_to_client', {'filepath': filepath, 'transcript': transcript})

@app.route('/upload', methods=['POST'])
def handle_upload():
    _file = request.files.get('file')
    if not _file or _file.filename == "":
        return redirect("/")

    filepath = os.path.join(STATIC_DIR, UPLOAD_DIR, _file.filename)
    _file.save(filepath)

    audio_signal, _ = librosa.load(filepath, sr=16000)

    model = get_vietasr()
    transcript = model.transcribe(audio_signal)

    return render_template("index.html", transcript=transcript, audiopath=filepath)

# KHÔNG chạy socketio.run khi deploy; gunicorn + eventlet sẽ dùng app/socketio