#!/usr/bin/env bash
set -e

# Thư mục lưu model
mkdir -p models/acoustic_model/vietnamese models/language_model configs

# Nếu biến ENV tồn tại, tải các file tương ứng
if [ -n "$ENCODER_URL" ]; then
  echo "Downloading encoder from $ENCODER_URL..."
  wget -q -O models/acoustic_model/vietnamese/Encoder-STEP-289936.pt "$ENCODER_URL"
fi

if [ -n "$DECODER_URL" ]; then
  echo "Downloading decoder from $DECODER_URL..."
  wget -q -O models/acoustic_model/vietnamese/Decoder-STEP-289936.pt "$DECODER_URL"
fi

if [ -n "$LM_URL" ]; then
  echo "Downloading language model from $LM_URL..."
  wget -q -O models/language_model/5-gram-lm.binary "$LM_URL"
fi

if [ -n "$CONFIG_URL" ]; then
  echo "Downloading config from $CONFIG_URL..."
  wget -q -O configs/quartznet12x1_vi.yaml "$CONFIG_URL"
fi

echo "Done downloading models (if any)."