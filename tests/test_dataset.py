from pathlib import Path
import tempfile
import unittest

from raspberry_face_recognition.dataset import (
    DatasetError,
    build_label_map,
    load_label_map,
    next_sample_index,
    normalize_person_name,
    save_label_map,
)


class DatasetTests(unittest.TestCase):
    def test_normalize_person_name_keeps_safe_names(self):
        self.assertEqual(normalize_person_name("Ada Lovelace"), "Ada_Lovelace")
        self.assertEqual(normalize_person_name("test.user-1"), "test.user-1")

    def test_normalize_person_name_rejects_empty_names(self):
        with self.assertRaises(DatasetError):
            normalize_person_name(" !!! ")

    def test_next_sample_index_ignores_non_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "000001.png").write_text("", encoding="utf-8")
            (root / "000007.jpg").write_text("", encoding="utf-8")
            (root / "notes.txt").write_text("", encoding="utf-8")

            self.assertEqual(next_sample_index(root), 8)

    def test_label_map_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            labels = build_label_map(["zeynep", "ali", "ali"])
            path = Path(temp_dir) / "labels.json"

            save_label_map(labels, path)

            self.assertEqual(load_label_map(path), {0: "ali", 1: "zeynep"})


if __name__ == "__main__":
    unittest.main()
