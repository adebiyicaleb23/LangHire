import os
import json
from pathlib import Path

# Paths
home = Path.home()
data_dir = home / ".local" / "share" / "LangHire"
data_dir.mkdir(parents=True, exist_ok=True)

root_dir = Path(__file__).resolve().parent.parent

# 1. Copy files to data_dir
for filename in ["candidate_profile.json", "settings.json", "resume.txt"]:
    src = root_dir / filename
    dst = data_dir / filename
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Copied {filename} to {dst}")

# 2. Update email from environment if present
email = os.environ.get("MY_EMAIL", "").strip()
if email:
    for profile_path in [data_dir / "candidate_profile.json", root_dir / "candidate_profile.json"]:
        if profile_path.exists():
            try:
                data = json.loads(profile_path.read_text(encoding="utf-8"))
                data["email"] = email
                profile_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                print(f"Updated email in {profile_path}")
            except Exception as e:
                print(f"Notice updating {profile_path}: {e}")

    for settings_path in [data_dir / "settings.json", root_dir / "settings.json"]:
        if settings_path.exists():
            try:
                data = json.loads(settings_path.read_text(encoding="utf-8"))
                if "sensitive_data" in data:
                    data["sensitive_data"]["email"] = email
                settings_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                print(f"Updated email in {settings_path}")
            except Exception as e:
                print(f"Notice updating {settings_path}: {e}")

print("Candidate environment prepared successfully.")
