"""
Packaging script for NASA Space Apps Challenge submission:
Creates a clean dr_d_space_apps_final.zip excluding:
- node_modules
- __pycache__
- .pytest_cache
- .venv / venv / env
- .git
- temporary files
"""

import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ZIP = PROJECT_ROOT / "dr_d_space_apps_final.zip"

EXCLUDE_DIRS = {
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".git",
    ".idea",
    ".vscode"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store"
}

EXCLUDE_FILES = {
    "dr_d_space_apps_final.zip"
}

def should_exclude(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    if path.name in EXCLUDE_FILES:
        return True
    return False

def create_submission_zip():
    print(f"Creating submission zip from: {PROJECT_ROOT}")
    print(f"Output destination: {OUTPUT_ZIP}")
    
    total_files = 0
    total_size = 0
    
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Modify dirs in-place to avoid descending into excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                if should_exclude(file_path):
                    continue
                
                rel_path = file_path.relative_to(PROJECT_ROOT)
                # Archive with root directory name for clean extraction
                arcname = Path("dr_d_astronaut_health") / rel_path
                
                zipf.write(file_path, arcname)
                total_files += 1
                total_size += file_path.stat().st_size

    zip_size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    raw_size_mb = total_size / (1024 * 1024)
    print(f"Packaging complete!")
    print(f"Files included: {total_files}")
    print(f"Uncompressed size: {raw_size_mb:.2f} MB")
    print(f"Final ZIP size: {zip_size_mb:.2f} MB")
    print(f"Archive created at: {OUTPUT_ZIP}")

if __name__ == "__main__":
    create_submission_zip()
