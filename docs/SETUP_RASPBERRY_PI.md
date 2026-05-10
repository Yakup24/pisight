# Raspberry Pi Setup

This project expects a Raspberry Pi with a working camera and Python 3.9 or newer.

## Install system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-opencv python3-numpy
```

OpenCV is installed from apt on purpose. It is usually more reliable on Raspberry Pi than installing camera-related OpenCV wheels from pip.

## Create the environment

```bash
python3 -m venv .venv --system-site-packages
. .venv/bin/activate
python -m pip install -e .
cp config.example.json config.json
```

The `--system-site-packages` flag lets the virtual environment use the OpenCV package installed by apt.

## Check the device

```bash
python -m raspberry_face_recognition --config config.json doctor
```

If the command reports that OpenCV is missing, confirm that `python3-opencv` is installed and that the virtual environment was created with `--system-site-packages`.

## Run as a service

Adjust the paths and user in `systemd/raspberry-face-recognition.service`, then install it:

```bash
sudo cp systemd/raspberry-face-recognition.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable raspberry-face-recognition
sudo systemctl start raspberry-face-recognition
```

Use `journalctl -u raspberry-face-recognition -f` to inspect runtime logs.
