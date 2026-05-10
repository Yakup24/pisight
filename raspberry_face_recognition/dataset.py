"""Dataset helpers for local face image storage."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Dict, Iterable, Iterator, Tuple

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


class DatasetError(RuntimeError):
    """Raised when the local face dataset cannot be used."""


def normalize_person_name(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "_", name.strip()).strip("_")
    if not cleaned:
        raise DatasetError("Person name must contain at least one letter or number.")
    return cleaned


def person_directory(faces_dir: Path, name: str) -> Path:
    return faces_dir / normalize_person_name(name)


def next_sample_index(directory: Path) -> int:
    highest = 0
    if not directory.exists():
        return 1
    for path in directory.iterdir():
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if path.stem.isdigit():
            highest = max(highest, int(path.stem))
    return highest + 1


def iter_person_images(faces_dir: Path) -> Iterator[Tuple[str, Path]]:
    if not faces_dir.exists():
        return
    for person_dir in sorted(path for path in faces_dir.iterdir() if path.is_dir()):
        person = person_dir.name
        for image_path in sorted(person_dir.iterdir()):
            if image_path.suffix.lower() in IMAGE_EXTENSIONS:
                yield person, image_path


def build_label_map(people: Iterable[str]) -> Dict[int, str]:
    unique_people = sorted(set(people))
    if not unique_people:
        raise DatasetError("No face images found. Run the collect command first.")
    return {index: person for index, person in enumerate(unique_people)}


def save_label_map(labels: Dict[int, str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {str(index): person for index, person in labels.items()}
    with path.open("w", encoding="utf-8") as handle:
        json.dump(serializable, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_label_map(path: Path) -> Dict[int, str]:
    if not path.exists():
        raise DatasetError(f"Label map not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {int(index): str(person) for index, person in data.items()}
