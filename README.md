# KL_ASR

Automatic Speech Recognition (ASR) Solution for Vietnamese Audio

## 🧭 Overview

KL_ASR là giải pháp nhận dạng giọng nói tiếng Việt (Vietnamese ASR)
chuyển âm thanh thành văn bản. Dự án tập trung vào huấn luyện mô hình,
triển khai inference và phát triển API/web.

## 🧩 Features

-   Chuyển audio → text\
-   Pipeline end-to-end\
-   Web/API tương tác\
-   Cấu hình linh hoạt\
-   Hỗ trợ mô hình pretrained hoặc fine‑tune

## 📁 Repository structure

    /configs/             
    /models/              
    /nemo/                
    /source_code/         
    /templates/           
    app.py                
    infer.py              
    requirements.txt      

## 🚀 Installation

    git clone https://github.com/phuc147aw/KL_ASR.git
    cd KL_ASR
    pip install -r requirements.txt

## 🧪 Usage

### CLI inference

    python infer.py --model_path models/your_model.ckpt --audio_path your_audio.wav

### Run web/API

    python app.py

## ⚙️ Configuration

Chỉnh trong `configs/config.yaml`.

## 🐳 Deploy on Render

This repository can be deployed to Render using Docker (CPU demo).

### Steps

1. Create a new **Web Service** on Render and connect this repository.
2. Select **Docker** as the runtime environment.
3. Set the following **Environment Variables**:
   - `ENCODER_URL`: URL to download the encoder checkpoint (e.g., from cloud storage)
   - `DECODER_URL`: URL to download the decoder checkpoint
   - `LM_URL`: URL to download the language model binary
   - `CONFIG_URL`: URL to download the config YAML file
   - `PRELOAD_MODEL`: Set to `1` to preload the model at startup (optional)
   - `SECRET_KEY`: Flask secret key (optional, defaults to `secret-key`)
4. Set the **Health Check Path** to `/health`.
5. Deploy the service.

### Notes

- The `start.sh` script will automatically download model files from the provided URLs before starting the server.
- Model files are not included in the repository to keep it lightweight.
- The `/health` endpoint returns `{"status": "healthy"}` for health checks.

## 📌 Technical highlight

-   NVIDIA NeMo\
-   Tokenization & acoustic modeling\
-   Tối ưu pipeline inference

## 📝 License

MIT License
