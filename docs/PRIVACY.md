# Privacy Notes

Face images and recognition models can expose personal information. Keep runtime data local unless there is a clear reason to move it.

## Local data

The project writes collected samples, trained models, and label maps under `data/` by default. That directory is ignored by Git.

Do not commit these files:

- collected face images
- trained model files
- label maps that connect names to model labels
- camera captures or debug frames

## Consent

Only collect face samples from people who know what the system is doing and agree to it. Avoid running recognition in shared spaces without a clear purpose and notice.

## Cleanup

To remove local training data, stop the service and delete the `data/` directory:

```bash
sudo systemctl stop raspberry-face-recognition
rm -rf data/
```

Train again from fresh samples when the dataset changes significantly.
