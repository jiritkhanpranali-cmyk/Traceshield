from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data"


def main():

    print("TraceShield AI - Dataset Inspector")
    print("=" * 50)

    if not DATA_DIR.exists():
        print("ERROR: Data directory does not exist.")
        return

    files = [
        file
        for file in DATA_DIR.iterdir()
        if file.is_file()
    ]

    if not files:
        print("No dataset files found.")
        print()
        print("Waiting for BCCC-DeFiFraudTrans-2025 dataset.")
        return

    print(f"Files found: {len(files)}")
    print()

    for file in files:

        print("-" * 50)
        print(f"File: {file.name}")
        print(f"Size: {file.stat().st_size / (1024 * 1024):.2f} MB")

        try:

            if file.suffix.lower() == ".csv":

                df = pd.read_csv(file, nrows=5)

            elif file.suffix.lower() in [".parquet", ".pq"]:

                df = pd.read_parquet(file)

            else:

                print("Unsupported file type.")
                continue

            print()
            print("Columns:")
            print(list(df.columns))

            print()
            print("Preview:")
            print(df.head())

        except Exception as error:

            print()
            print("Could not inspect file.")
            print("Error:", error)

    print()
    print("=" * 50)
    print("Dataset inspection complete.")


if __name__ == "__main__":
    main()
