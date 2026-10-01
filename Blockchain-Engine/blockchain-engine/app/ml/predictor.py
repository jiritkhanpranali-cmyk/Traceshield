from pathlib import Path

from ml.model import create_model


DATA_DIR = Path(__file__).resolve().parent / "data"
MODEL_PATH = Path(__file__).resolve().parent / "trained_model.joblib"


def main():

    print("TraceShield AI - ML Training")

    print("Data directory:")
    print(DATA_DIR)

    print("Model output:")
    print(MODEL_PATH)

    if not DATA_DIR.exists():
        print("ERROR: Training data directory not found.")
        return

    files = list(DATA_DIR.iterdir())

    if not files:
        print("Training data is not available yet.")
        print("Waiting for BCCC-DeFiFraudTrans-2025 dataset.")
        return

    model = create_model()

    print("Random Forest model created successfully.")
    print(model)

    print("Dataset detected.")
    print("Next step: inspect dataset columns and labels before training.")


if __name__ == "__main__":
    main()