#!/bin/bash
# Download model files from URLs provided via environment variables
# into models/ and configs/ directories.

set -e

echo "=== Downloading model files ==="

# Create directories if they don't exist
mkdir -p models/acoustic_model/vietnamese
mkdir -p models/language_model
mkdir -p configs

# Download encoder checkpoint
if [ -n "$ENCODER_URL" ]; then
    echo "Downloading encoder from $ENCODER_URL..."
    curl -L -o models/acoustic_model/vietnamese/Encoder-STEP-289936.pt "$ENCODER_URL"
else
    echo "ENCODER_URL not set, skipping encoder download."
fi

# Download decoder checkpoint
if [ -n "$DECODER_URL" ]; then
    echo "Downloading decoder from $DECODER_URL..."
    curl -L -o models/acoustic_model/vietnamese/Decoder-STEP-289936.pt "$DECODER_URL"
else
    echo "DECODER_URL not set, skipping decoder download."
fi

# Download language model
if [ -n "$LM_URL" ]; then
    echo "Downloading language model from $LM_URL..."
    curl -L -o models/language_model/5-gram-lm.binary "$LM_URL"
else
    echo "LM_URL not set, skipping language model download."
fi

# Download config file
if [ -n "$CONFIG_URL" ]; then
    echo "Downloading config from $CONFIG_URL..."
    curl -L -o configs/quartznet12x1_vi.yaml "$CONFIG_URL"
else
    echo "CONFIG_URL not set, skipping config download."
fi

echo "=== Model download complete ==="
