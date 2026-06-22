import pandas as pd
from pathlib import Path

# Project root
project_root = Path(__file__).resolve().parents[2]

raw_path = project_root / "data" / "raw"
processed_path = project_root / "data" / "processed"

# Create processed folder if not exists
processed_path.mkdir(parents=True, exist_ok=True)

for file in raw_path.glob("*.xlsx"):
    df = pd.read_excel(file, header=1)

    output_file = processed_path / f"{file.stem}_cleaned.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name}")