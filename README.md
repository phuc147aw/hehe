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

## 📌 Technical highlight

-   NVIDIA NeMo\
-   Tokenization & acoustic modeling\
-   Tối ưu pipeline inference

## 📝 License

MIT License
