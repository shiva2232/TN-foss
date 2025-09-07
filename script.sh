#!/bin/sh
sudo apt install tesseract-ocr # running in linux
python3 -m venv venv
. venv/bin/activate && pip3 install -r requirements.txt
mkdir voice
cd voice
for url in \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx?download=true" \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json?download=true" \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/MODEL_CARD?download=true"
do
  fname=$(basename "${url%%\?*}")   # strip query string
  echo "Downloading $fname ..."
  wget -O "$fname" "$url"
done
cd ..