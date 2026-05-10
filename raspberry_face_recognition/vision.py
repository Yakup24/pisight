"""OpenCV integration points for detection and recognition."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def require_cv2() -> Any:
    try:
        import cv2  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "OpenCV is not installed. On Raspberry Pi, run: sudo apt install python3-opencv"
        ) from exc
    return cv2


def require_numpy() -> Any:
    try:
        import numpy as np  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("NumPy is not installed. Run: python3 -m pip install -r requirements.txt") from exc
    return np


def default_cascade_path(cv2: Any) -> Path:
    return Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"


def create_detector(config: Any) -> Any:
    cv2 = require_cv2()
    cascade_path = Path(config.cascade_path).expanduser() if config.cascade_path else default_cascade_path(cv2)
    detector = cv2.CascadeClassifier(str(cascade_path))
    if detector.empty():
        raise RuntimeError(f"Could not load Haar cascade: {cascade_path}")
    return detector


def create_recognizer() -> Any:
    cv2 = require_cv2()
    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "OpenCV face recognizer support is missing. Install the contrib build or python3-opencv."
        )
    return cv2.face.LBPHFaceRecognizer_create()


def detect_faces(frame: Any, detector: Any, config: Any) -> tuple[Any, Any]:
    cv2 = require_cv2()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=config.scale_factor,
        minNeighbors=config.min_neighbors,
        minSize=(config.face_width, config.face_height),
    )
    return gray, faces


def crop_face(gray_frame: Any, face: tuple[int, int, int, int], size: tuple[int, int]) -> Any:
    cv2 = require_cv2()
    x, y, width, height = face
    crop = gray_frame[y : y + height, x : x + width]
    return cv2.resize(crop, size)
