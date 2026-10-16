
from pathlib import Path

# ==================================================
# PROJECT ROOT
# ==================================================

PROJECT_ROOT = Path.cwd()

# ==================================================
# DEFINE PROJECT FILES
# ==================================================

files = [
    "README.md",
    ".gitignore",
    "requirements.txt",
    ".env.example",

    # Data
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/reference/.gitkeep",

    # Notebooks
    "notebooks/01_data_understanding.ipynb",
    "notebooks/02_eda.ipynb",
    "notebooks/03_feature_engineering.ipynb",
    "notebooks/04_model_training.ipynb",
    "notebooks/05_model_evaluation.ipynb",

    # Source code
    "src/__init__.py",
    "src/data_processing.py",
    "src/features.py",
    "src/train.py",
    "src/evaluate.py",
    "src/predict.py",

    # Models
    "models/production/.gitkeep",
    "models/candidates/.gitkeep",

    # Backend
    "backend/__init__.py",
    "backend/main.py",
    "backend/schemas.py",

    # Frontend
    "frontend/README.md",

    # MLOps
    "mlops/monitoring/reports/.gitkeep",

    # Artifacts
    "artifacts/metrics/.gitkeep",
    "artifacts/plots/.gitkeep",
    "artifacts/reports/.gitkeep",

    # Tests
    "tests/test_data_processing.py",
    "tests/test_api.py",
]

# ==================================================
# CREATE FILES AND PARENT DIRECTORIES
# ==================================================

for file in files:
    path = PROJECT_ROOT / file

    # Create parent directories
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create empty files without overwriting existing files
    if not path.exists():
        if file.endswith(".ipynb"):
            path.write_text(
                '{"cells":[],"metadata":{},'
                '"nbformat":4,"nbformat_minor":5}',
                encoding="utf-8"
            )
        else:
            path.touch()

    print(f"Created: {path}")

# ==================================================
# FINAL MESSAGE
# ==================================================

print("\n" + "=" * 60)
print("FRAUD DETECTION PROJECT CREATED SUCCESSFULLY!")
print("=" * 60)

print(f"\nProject location: {PROJECT_ROOT}")
print("\nNext steps:")
print("1. Create a virtual environment")
print("2. Install Python libraries")
print("3. Add the fraud detection dataset")
print("4. Perform data cleaning and EDA")
print("5. Train and evaluate ML models")
print("6. Build a FastAPI backend")
print("7. Build a React frontend")
print("8. Add model monitoring")
