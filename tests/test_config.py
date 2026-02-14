"""Tests for the new LabDataConfig."""

import pytest
import yaml
import tempfile
from pathlib import Path

from labdata.config import LabDataConfig, BibFile


class TestLabDataConfig:
    def test_from_yaml(self, tmp_path):
        config_data = {
            "bib_dir": "data/bib",
            "bib_files": [
                {"name": "journal.bib", "category": "Journal Papers"},
                {"name": "conf.bib", "category": "Conference Papers"},
            ],
            "pdf_base_url": "https://example.com/pdfs",
            "people_file": "data/people.yaml",
            "projects_file": "data/projects.yaml",
        }
        config_path = tmp_path / "lab.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)

        config = LabDataConfig.from_yaml(str(config_path))
        assert config.bib_dir == "data/bib"
        assert len(config.bib_files) == 2
        assert config.bib_files[0].name == "journal.bib"
        assert config.bib_files[0].category == "Journal Papers"
        assert config.pdf_base_url == "https://example.com/pdfs"
        assert config.people_file == "data/people.yaml"
        assert config.projects_file == "data/projects.yaml"

    def test_minimal_config(self, tmp_path):
        config_data = {
            "bib_dir": "bib",
            "bib_files": [
                {"name": "pubs.bib", "category": "Publications"},
            ],
        }
        config_path = tmp_path / "lab.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)

        config = LabDataConfig.from_yaml(str(config_path))
        assert config.bib_dir == "bib"
        assert config.pdf_base_url is None
        assert config.people_file is None
        assert config.projects_file is None

    def test_bib_file_dataclass(self):
        bf = BibFile(name="test.bib", category="Test")
        assert bf.name == "test.bib"
        assert bf.category == "Test"
