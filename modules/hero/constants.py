from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED = {"image/png": ".png", "image/jpeg": ".jpg"}
MAX_SIZE = 2 * 1024 * 1024  # 2MB
