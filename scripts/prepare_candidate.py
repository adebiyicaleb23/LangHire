import os
import sys
import json
from pathlib import Path

# Add project root to sys.path so backend imports work
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from backend.core.config import get_data_dir

data_dir = get_data_dir()
data_dir.mkdir(parents=True, exist_ok=True)
print(f"Target OS Data Directory: {data_dir}")

# 1. Load candidate profile from root or generate if needed
candidate_profile_file = root_dir / "candidate_profile.json"
if candidate_profile_file.exists():
    profile = json.loads(candidate_profile_file.read_text(encoding="utf-8"))
else:
    profile = {}

# Ensure required fields exist
if not profile.get("target_locations"):
    profile["target_locations"] = ["Remote", "Worldwide"]
if not profile.get("target_job_titles"):
    profile["target_job_titles"] = ["AI Trainer", "AI Data Evaluator", "RLHF Specialist"]

email = os.environ.get("MY_EMAIL", "").strip()
if email:
    profile["email"] = email

# Save candidate_profile to data_dir and root
profile_bytes = json.dumps(profile, indent=2)
(data_dir / "candidate_profile.json").write_text(profile_bytes, encoding="utf-8")
candidate_profile_file.write_text(profile_bytes, encoding="utf-8")
print(f"Saved candidate_profile.json to {data_dir} and root.")

# 2. Settings
settings = {
    "resume_path": str(root_dir / "resume.txt"),
    "blocked_domains": ["meeboss.com"],
    "sensitive_data": {
        "email": email or profile.get("email", "adebiyicaleb222@gmail.com"),
        "password": ""
    },
    "max_failures": 8,
    "stagger_delay": 5,
    "data_dir": str(data_dir),
    "telemetry_enabled": False,
    "theme": "system"
}
settings_bytes = json.dumps(settings, indent=2)
(data_dir / "settings.json").write_text(settings_bytes, encoding="utf-8")
(root_dir / "settings.json").write_text(settings_bytes, encoding="utf-8")
print(f"Saved settings.json to {data_dir} and root.")

# 3. LLM Settings (Gemini)
gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_ACCESS") or os.environ.get("GEMINI_API_NAME") or ""
model = os.environ.get("LLM_MODEL", "gemini-2.0-flash")

llm_settings = {
    "provider": "gemini",
    "gemini": {
        "api_key": gemini_key,
        "model": model
    },
    "openai": {"api_key": "", "model": "gpt-4o"},
    "anthropic": {"api_key": "", "model": "claude-sonnet-4-5"}
}
llm_bytes = json.dumps(llm_settings, indent=2)
(data_dir / "llm_settings.json").write_text(llm_bytes, encoding="utf-8")
(root_dir / "llm_settings.json").write_text(llm_bytes, encoding="utf-8")
print(f"Saved llm_settings.json to {data_dir} and root.")

# Also ensure resume.txt is copied
resume_file = root_dir / "resume.txt"
if resume_file.exists():
    (data_dir / "resume.txt").write_text(resume_file.read_text(encoding="utf-8"), encoding="utf-8")

print("All candidate, settings, and LLM configurations prepared successfully.")
