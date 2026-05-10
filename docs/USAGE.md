# PiSight Usage

The workflow has three steps: collect samples, train a model, then run recognition.

## 1. Check the setup

```bash
pisight --config config.json doctor
```

This checks the config file, OpenCV import, Haar cascade loading, and LBPH recognizer support.

## 2. Collect face samples

```bash
pisight --config config.json collect --name person_name
```

Collected images are saved under `data/faces/<person_name>/`. The `data/` directory is ignored by Git because it may contain personal data.

You can change the sample count for one run:

```bash
pisight --config config.json collect --name person_name --count 60
```

## 3. Train the recognizer

```bash
pisight --config config.json train
```

Training writes two local files:

- `data/model.yml`
- `data/labels.json`

Both are local runtime artifacts and should not be committed.

## 4. Run recognition

```bash
pisight --config config.json recognize
```

The recognizer shows the predicted name and confidence score on the camera preview. Lower LBPH confidence is usually better. The `confidence_threshold` value in `config.json` controls when a prediction is treated as unknown.
