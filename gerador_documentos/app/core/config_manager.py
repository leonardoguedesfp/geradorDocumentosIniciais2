"""Read/write config.json for persistent settings."""

import json
import os
import sys


def _get_config_path() -> str:
    """Return path to config.json next to the executable (or main.py)."""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    return os.path.join(base, "config.json")


def load_config() -> dict:
    """Load config from config.json. Returns dict with available keys."""
    path = _get_config_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(config: dict) -> None:
    """Save config dict to config.json."""
    path = _get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_templates_folder(config: dict | None = None) -> str:
    """Return configured templates folder or empty string."""
    if config is None:
        config = load_config()
    return config.get("templates_folder", "")


def get_output_folder(config: dict | None = None) -> str:
    """Return configured output folder or empty string."""
    if config is None:
        config = load_config()
    return config.get("output_folder", "")
