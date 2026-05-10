# Raspberry Face Recognition

A small Raspberry Pi face-recognition project built around OpenCV. The project keeps the workflow simple: collect face samples, train a local recognizer, then run recognition from a camera stream.

The code is designed for a local device. It does not upload camera frames or face data to a remote service.

## What It Does

- captures labeled face samples from a Raspberry Pi camera or USB camera
- trains an OpenCV LBPH face recognizer from the local dataset
- runs live recognition with configurable confidence thresholds
- stores datasets and trained models on disk
- includes a basic systemd service template for running on boot

## Repository Layout

```text
raspberry_face_recognition/  Python package and CLI
config.example.json          Example runtime configuration
scripts/install_pi.sh        Raspberry Pi setup helper
systemd/                     Optional service template
tests/                       Unit tests for non-camera code
```

## Install

On Raspberry Pi OS, prefer system packages for OpenCV:

```sh
sudo apt update
sudo apt install -y python3-opencv python3-numpy python3-pip
python3 -m pip install -r requirements.txt
```

For the LBPH recognizer, your OpenCV build must include the `cv2.face` module. If it is missing, install an OpenCV contrib package/build for your platform.

## Quick Start

Copy the example config:

```sh
cp config.example.json config.json
```

Check the environment:

```sh
python3 -m raspberry_face_recognition doctor --config config.json
```

Collect samples for a person:

```sh
python3 -m raspberry_face_recognition collect --config config.json --name yakup
```

Train the recognizer:

```sh
python3 -m raspberry_face_recognition train --config config.json
```

Run live recognition:

```sh
python3 -m raspberry_face_recognition recognize --config config.json
```

## Data

By default, local runtime files are stored under `data/`:

- `data/faces/` contains captured face crops
- `data/model.yml` contains the trained recognizer
- `data/labels.json` maps numeric IDs to names

These files are ignored by Git because they may contain personal biometric data.

## Development

Run tests that do not require a camera:

```sh
python3 -m unittest discover -s tests -p "test_*.py"
```

## Privacy Note

Face images are sensitive data. Keep datasets local, avoid committing captured faces, and get consent before collecting samples from other people.
