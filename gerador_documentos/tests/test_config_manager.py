"""Tests for config_manager: save, load, missing keys, missing file."""

import json
import os
import sys
import tempfile
import shutil

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core import config_manager


@pytest.fixture
def config_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(autouse=True)
def patch_config_path(config_dir, monkeypatch):
    """Patch _get_config_path to use temp directory."""
    config_path = os.path.join(config_dir, "config.json")
    monkeypatch.setattr(config_manager, "_get_config_path", lambda: config_path)
    return config_path


class TestLoadConfig:
    def test_missing_file(self):
        result = config_manager.load_config()
        assert result == {}

    def test_valid_config(self, patch_config_path):
        data = {"templates_folder": "/tmp/templates", "output_folder": "/tmp/output"}
        with open(patch_config_path, "w") as f:
            json.dump(data, f)

        result = config_manager.load_config()
        assert result["templates_folder"] == "/tmp/templates"
        assert result["output_folder"] == "/tmp/output"

    def test_corrupted_json(self, patch_config_path):
        with open(patch_config_path, "w") as f:
            f.write("{invalid json")

        result = config_manager.load_config()
        assert result == {}

    def test_non_dict_json(self, patch_config_path):
        with open(patch_config_path, "w") as f:
            json.dump([1, 2, 3], f)

        result = config_manager.load_config()
        assert result == {}


class TestSaveConfig:
    def test_save_and_reload(self, patch_config_path):
        data = {"templates_folder": "/path/a", "output_folder": "/path/b"}
        config_manager.save_config(data)

        with open(patch_config_path) as f:
            loaded = json.load(f)
        assert loaded == data

    def test_save_overwrites(self, patch_config_path):
        config_manager.save_config({"templates_folder": "/old"})
        config_manager.save_config({"templates_folder": "/new"})

        result = config_manager.load_config()
        assert result["templates_folder"] == "/new"


class TestGetters:
    def test_get_templates_folder_present(self):
        config = {"templates_folder": "/my/path"}
        assert config_manager.get_templates_folder(config) == "/my/path"

    def test_get_templates_folder_absent(self):
        assert config_manager.get_templates_folder({}) == ""

    def test_get_output_folder_present(self):
        config = {"output_folder": "/out"}
        assert config_manager.get_output_folder(config) == "/out"

    def test_get_output_folder_absent(self):
        assert config_manager.get_output_folder({}) == ""

    def test_get_templates_folder_from_file(self, patch_config_path):
        config_manager.save_config({"templates_folder": "/saved/path"})
        assert config_manager.get_templates_folder() == "/saved/path"

    def test_get_output_folder_missing_key(self, patch_config_path):
        config_manager.save_config({"templates_folder": "/only/this"})
        assert config_manager.get_output_folder() == ""
