import json
from pathlib import Path

VALID_CLOUDS = {"aws", "azure"}

STATE_FILE = Path(__file__).resolve().parents[1] / "state" / "cloud_state.json"


def ensure_state_file_exists() -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not STATE_FILE.exists():
        write_active_cloud("aws")


def read_cloud_state() -> dict:
    ensure_state_file_exists()

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_active_cloud() -> str:
    state = read_cloud_state()
    active_cloud = state.get("active_cloud", "aws")

    if active_cloud not in VALID_CLOUDS:
        return "aws"

    return active_cloud


def write_active_cloud(cloud: str) -> dict:
    if cloud not in VALID_CLOUDS:
        raise ValueError(f"Cloud no soportada: {cloud}")

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    state = {
        "active_cloud": cloud,
    }

    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)

    return state


def get_available_clouds() -> list[str]:
    return sorted(VALID_CLOUDS)