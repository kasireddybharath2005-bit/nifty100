from pathlib import Path

raw_path = Path(r"C:\Users\kasir\PycharmProjects\PythonProject4\data\raw")

files = list(raw_path.glob("*.xlsx"))

print("Files Found:", len(files))

for file in files:
    print(file.name)

