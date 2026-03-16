"""Tests for automatic output folder creation (saida/YYYY-MM-DD_HH-MM-SS/)."""

import os
import re
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.output_manager import create_output_folder, get_base_dir


class TestGetBaseDir:
    def test_returns_existing_directory(self):
        base = get_base_dir()
        assert os.path.isdir(base)


class TestCreateOutputFolder:
    def test_creates_saida_subfolder(self, monkeypatch, tmp_dir):
        """Each call creates saida/YYYY-MM-DD_HH-MM-SS/ inside the base dir."""
        monkeypatch.setattr(
            "app.core.output_manager.get_base_dir", lambda: tmp_dir
        )
        folder = create_output_folder()

        assert os.path.isdir(folder)

        rel = os.path.relpath(folder, tmp_dir)
        parts = rel.split(os.sep)
        assert parts[0] == "saida"
        assert re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", parts[1])

    def test_each_call_creates_new_folder(self, monkeypatch, tmp_dir):
        """Two calls with different timestamps create separate folders."""
        monkeypatch.setattr(
            "app.core.output_manager.get_base_dir", lambda: tmp_dir
        )
        folder1 = create_output_folder()
        time.sleep(1.1)
        folder2 = create_output_folder()

        assert folder1 != folder2
        assert os.path.isdir(folder1)
        assert os.path.isdir(folder2)

    def test_files_appear_in_timestamped_folder(self, monkeypatch, tmp_dir, templates_dir, sample_client_data):
        """Generated files end up inside the timestamped subfolder."""
        monkeypatch.setattr(
            "app.core.output_manager.get_base_dir", lambda: tmp_dir
        )
        from app.core.placeholder_engine import generate_documents
        from app.core.template_loader import load_default_templates

        output_folder = create_output_folder()
        templates = load_default_templates(templates_dir)

        results = generate_documents(
            sample_client_data, templates, ["procuracao"], output_folder,
        )

        assert len(results) == 1
        assert results[0]["success"]
        assert os.path.isfile(results[0]["path"])
        assert results[0]["path"].startswith(output_folder)

        rel = os.path.relpath(results[0]["path"], tmp_dir)
        parts = rel.split(os.sep)
        assert parts[0] == "saida"
        assert re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", parts[1])
        assert parts[2].endswith(".docx")
