"""Automatic output folder creation — saida/YYYY-MM-DD_HH-MM-SS/."""

import os
import sys
from datetime import datetime


def get_base_dir() -> str:
    """Return directory next to the executable (or main.py in dev)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(os.path.join(__file__, "..", "..", "..")))


def create_output_folder() -> str:
    """Create and return saida/YYYY-MM-DD_HH-MM-SS/ next to the executable."""
    base = get_base_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = os.path.join(base, "saida", timestamp)
    os.makedirs(folder, exist_ok=True)
    return folder
