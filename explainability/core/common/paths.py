from pathlib import Path

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]  # .../XAIEvaluator/core/common -> root

def prompt_dir() -> Path:
    return project_root() / "prompt"

def data_dir() -> Path:
    return project_root() / "data"
