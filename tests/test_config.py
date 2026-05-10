from pathlib import Path
import json
import tempfile
import unittest

from raspberry_face_recognition.config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_config_resolves_paths_relative_to_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_path = root / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "data_dir": "runtime",
                        "faces_dir": "runtime/faces",
                        "model_path": "runtime/model.yml",
                        "labels_path": "runtime/labels.json",
                        "sample_count": 12,
                        "display": False,
                    }
                ),
                encoding="utf-8",
            )

            config = load_config(str(config_path))

            self.assertEqual(config.data_dir, (root / "runtime").resolve())
            self.assertEqual(config.faces_dir, (root / "runtime/faces").resolve())
            self.assertEqual(config.model_path, (root / "runtime/model.yml").resolve())
            self.assertEqual(config.labels_path, (root / "runtime/labels.json").resolve())
            self.assertEqual(config.sample_count, 12)
            self.assertFalse(config.display)

    def test_missing_config_uses_defaults(self):
        config = load_config("missing-config.json")

        self.assertEqual(config.camera_index, 0)
        self.assertEqual(config.face_size, (160, 160))
        self.assertEqual(config.sample_count, 40)


if __name__ == "__main__":
    unittest.main()
