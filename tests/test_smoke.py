"""Smoke tests to verify the package loads and basic functionality works."""

import labdata


def test_package_imports():
    """Verify the package can be imported and has expected attributes."""
    assert hasattr(labdata, '__version__')
    assert labdata.__version__ == "2.0.0-dev"


def test_core_classes_importable():
    """Verify core classes are importable from the package."""
    from labdata import (
        LibraryConfig,
        Publication,
        PublicationsConfig,
        list_publications,
        export_to_yaml,
        export_to_json,
    )


def test_publication_dataclass():
    """Verify Publication dataclass works."""
    from labdata import Publication

    pub = Publication(
        entry_type="Journal Papers",
        year=2024,
        title="Test Paper",
        authors="J. Doe and J. Smith",
        venue="Test Journal, 2024",
        note="",
        pdf_url=None,
        projects=["test_project"],
    )
    assert pub.year == 2024
    assert pub.title == "Test Paper"
    assert pub.projects == ["test_project"]

    d = pub.to_dict()
    assert d["title"] == "Test Paper"
    assert d["year"] == 2024
