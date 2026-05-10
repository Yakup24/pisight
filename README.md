# PiSight

PiSight is a Raspberry Pi face-recognition toolkit built around OpenCV. The workflow is intentionally small: collect face samples, train a local recognizer, then run recognition from a camera stream.

The project is designed for local devices. It does not upload camera frames, face samples, labels, or trained models to a remote service.

## What It Does

- captures labeled face samples from a Raspberry Pi camera or USB camera
- trains an OpenCV LBPH face recognizer from a local dataset
- runs live recognition with configurable confidence thresholds
- stores datasets and trained models on disk
- includes setup notes, tests, and a systemd service template

## Repository Layout

```text
raspberry_face_recognition/  PiSight Python package and CLI
config.example.json          Example runtime configuration
docs/                        Setup, usage, and privacy notes
scripts/install_pi.sh        Raspberry Pi setup helper
systemd/                     Optional service template
tests/                       Unit tests for non-camera code
```

## Install

On Raspberry Pi OS, prefer system packages for OpenCV:

```sh
sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-opencv python3-numpy
python3 -m venv .venv --system-site-packages
. .venv/bin/activate
python -m pip install -e .
cp config.example.json config.json
```

The `--system-site-packages` flag lets the virtual environment use the OpenCV package installed by apt.

## Quick Start

Check the environment:

```sh
pisight --config config.json doctor
```

Collect samples for a person:

```sh
pisight --config config.json collect --name person_name
```

Train the recognizer:

```sh
pisight --config config.json train
```

Run live recognition:

```sh
pisight --config config.json recognize
```

## Data

By default, local runtime files are stored under `data/`:

- `data/faces/` contains captured face crops
- `data/model.yml` contains the trained recognizer
- `data/labels.json` maps numeric IDs to names

These files are ignored by Git because they may contain personal biometric data.

## Documentation

- [Raspberry Pi setup](docs/SETUP_RASPBERRY_PI.md)
- [Usage guide](docs/USAGE.md)
- [Privacy notes](docs/PRIVACY.md)

## Development

Run tests that do not require a camera:

```sh
python -m unittest discover -s tests
```
