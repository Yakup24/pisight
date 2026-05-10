#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y \
  python3 \
  python3-numpy \
  python3-opencv \
  python3-pip \
  python3-venv

python3 -m venv .venv --system-site-packages
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

if [ ! -f config.json ]; then
  cp config.example.json config.json
fi

python -m raspberry_face_recognition --config config.json doctor
