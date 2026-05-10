"""Configuration loading for the face recognition commands."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class AppConfig:
    camera_index: int = 0
    data_dir: Path = Path("data")
    faces_dir: Path = Path("data/faces")
    model_path: Path = Path("data/model.yml")
    labels_path: Path = Path("data/labels.json")
    cascade_path: str = ""
    sample_count: int = 40
    face_width: int = 160
    face_height: int = 160
    scale_factor: float = 1.2
    min_neighbors: int = 5
    min_face_size: int = 60
    confidence_threshold: float = 70.0
    display: bool = True

    @property
    def face_size(self) -> tuple[int, int]:
        return (self.face_width, self.face_height)


def _resolve_path(value: Any, base_dir: Path) -> Path:
    path = Path(str(value)).expanduser()
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def _read_json(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Configuration must be a JSON object: {path}")
    return data


def load_config(path: Optional[str] = None) -> AppConfig:
    """Load configuration from JSON, falling back to safe defaults."""
    config_path = Path(path or "config.json").expanduser()
    base_dir = config_path.parent.resolve() if config_path.exists() else Path.cwd()
    data = _read_json(config_path)

    return AppConfig(
        camera_index=int(data.get("camera_index", AppConfig.camera_index)),
        data_dir=_resolve_path(data.get("data_dir", AppConfig.data_dir), base_dir),
        faces_dir=_resolve_path(data.get("faces_dir", AppConfig.faces_dir), base_dir),
        model_path=_resolve_path(data.get("model_path", AppConfig.model_path), base_dir),
        labels_path=_resolve_path(data.get("labels_path", AppConfig.labels_path), base_dir),
        cascade_path=str(data.get("cascade_path", AppConfig.cascade_path)),
        sample_count=int(data.get("sample_count", AppConfig.sample_count)),
        face_width=int(data.get("face_width", AppConfig.face_width)),
        face_height=int(data.get("face_height", AppConfig.face_height)),
        scale_factor=float(data.get("scale_factor", AppConfig.scale_factor)),
        min_neighbors=int(data.get("min_neighbors", AppConfig.min_neighbors)),
        min_face_size=int(data.get("min_face_size", AppConfig.min_face_size)),
        confidence_threshold=float(data.get("confidence_threshold", AppConfig.confidence_threshold)),
        display=bool(data.get("display", AppConfig.display)),
    )
