from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
GITHUB_WORKFLOWS_DIR = BASE_DIR.parent / ".github" / "workflows"
CUSTOM_PIPELINE_FILE = GITHUB_WORKFLOWS_DIR / "custom.yml"
DEFAULT_PIPELINE_FILE = GITHUB_WORKFLOWS_DIR / "default.yml"

AVAILABLE_STEPS = {
    "python": ["build", "test", "deploy"],
    "node": ["build", "test", "deploy"]
}