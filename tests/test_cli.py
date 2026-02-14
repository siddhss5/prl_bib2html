"""Tests for the CLI."""

import json
import yaml
import pytest
import subprocess
import sys
from pathlib import Path


FIXTURES = Path(__file__).parent / "fixtures"


def run_cli(*args):
    """Run labdata CLI and return CompletedProcess."""
    return subprocess.run(
        [sys.executable, "-m", "labdata.cli", *args],
        capture_output=True, text=True,
    )


class TestCLIOutput:
    def test_yaml_output(self, tmp_path):
        out = str(tmp_path / "lab.yml")
        result = run_cli(
            "--config", str(FIXTURES / "lab.yaml"),
            "--output", out,
        )
        assert result.returncode == 0
        assert Path(out).exists()
        with open(out, 'r') as f:
            data = yaml.safe_load(f)
        assert len(data["publications"]) == 3
        assert "Wrote" in result.stdout

    def test_json_output(self, tmp_path):
        out = str(tmp_path / "lab.json")
        result = run_cli(
            "--config", str(FIXTURES / "lab.yaml"),
            "--format", "json",
            "--output", out,
        )
        assert result.returncode == 0
        with open(out, 'r') as f:
            data = json.load(f)
        assert "publications" in data
        assert "people" in data
        assert "projects" in data

    def test_missing_config(self):
        result = run_cli("--config", "/nonexistent/lab.yaml", "--output", "/tmp/out.yml")
        assert result.returncode != 0
        assert "not found" in result.stderr

    def test_no_output_arg(self):
        result = run_cli("--config", str(FIXTURES / "lab.yaml"))
        assert result.returncode != 0


class TestCLIValidate:
    def test_validate_passes(self):
        result = run_cli(
            "--config", str(FIXTURES / "lab.yaml"),
            "--validate",
        )
        assert result.returncode == 0
        assert "Publications: 3" in result.stdout
        assert "People: 3" in result.stdout
        assert "Projects: 2" in result.stdout
        assert "Validation passed" in result.stdout

    def test_validate_shows_unresolved(self):
        """The fixture has an external author (E. E. Jones) who is unresolved."""
        result = run_cli(
            "--config", str(FIXTURES / "lab.yaml"),
            "--validate",
        )
        # E. E. Jones is in sample.bib but not in people.yaml
        assert "Unresolved authors" in result.stdout


class TestCLIUnresolved:
    def test_unresolved_list(self):
        result = run_cli(
            "--config", str(FIXTURES / "lab.yaml"),
            "--unresolved",
        )
        assert result.returncode == 0
        assert "E. E. Jones" in result.stdout

    def test_unresolved_without_people(self, tmp_path):
        """Without people_file, no authors can be resolved, but unresolved list is empty
        (no people to match against → nothing to report)."""
        config_data = {
            "bib_dir": str(FIXTURES),
            "bib_files": [{"name": "sample.bib", "category": "Test"}],
        }
        config_path = tmp_path / "minimal.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)

        result = run_cli("--config", str(config_path), "--unresolved")
        assert result.returncode == 0
        assert "All authors resolved" in result.stdout
