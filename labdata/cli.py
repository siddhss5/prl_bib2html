"""
Command-line interface for labdata.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import argparse
import sys
from pathlib import Path

from .config import LabDataConfig
from .assembler import assemble
from .exporters import export_to_yaml, export_to_json


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Assemble academic lab data from BibTeX and YAML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate YAML output
  labdata --config lab.yaml --output _data/lab.yml

  # Generate JSON output
  labdata --config lab.yaml --format json --output lab.json

  # Validate configuration and data
  labdata --config lab.yaml --validate

  # Show unresolved author names
  labdata --config lab.yaml --unresolved
        """
    )

    parser.add_argument(
        '--config', required=True,
        help='Path to YAML configuration file (lab.yaml)'
    )
    parser.add_argument(
        '--format', choices=['yaml', 'json'], default='yaml',
        help='Output format (default: yaml)'
    )
    parser.add_argument(
        '--output',
        help='Output file path'
    )
    parser.add_argument(
        '--validate', action='store_true',
        help='Validate configuration and report issues, then exit'
    )
    parser.add_argument(
        '--unresolved', action='store_true',
        help='Show unresolved author names, then exit'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.output and not args.validate and not args.unresolved:
        parser.error("One of --output, --validate, or --unresolved is required")

    # Load configuration
    try:
        config = LabDataConfig.from_yaml(args.config)
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)

    # Assemble data (manual pipeline to capture unresolved/unknown for reporting)
    from .parsers.bibtex import parse_all_publications
    from .loaders import load_people, load_projects
    from .resolver import resolve_authors, resolve_projects, compute_backlinks
    from .models import LabData, Collaborator

    bib_files = [{'name': bf.name, 'category': bf.category} for bf in config.bib_files]
    publications = parse_all_publications(
        bib_dir=config.bib_dir,
        bib_files=bib_files,
        pdf_base_url=config.pdf_base_url,
    )

    people = load_people(config.people_file) if config.people_file else []
    projects = load_projects(config.projects_file) if config.projects_file else []

    unresolved_authors = resolve_authors(publications, people)
    unknown_projects = resolve_projects(publications, projects)

    collab_counts = {}
    collab_years = {}
    for pub in publications:
        for author in pub.authors:
            if author.person_id is None:
                collab_counts[author.name] = collab_counts.get(author.name, 0) + 1
                collab_years[author.name] = max(collab_years.get(author.name, 0), pub.year)
    collaborators = sorted(
        [Collaborator(name=name, publication_count=collab_counts[name],
                      last_year=collab_years[name])
         for name in collab_counts],
        key=lambda c: (-c.last_year, -c.publication_count, c.name),
    )

    data = LabData(
        publications=publications, people=people,
        projects=projects, collaborators=collaborators,
    )
    compute_backlinks(data)

    # --validate mode
    if args.validate:
        errors = 0
        print(f"Publications: {len(data.publications)}")
        print(f"People: {len(data.people)}")
        print(f"Projects: {len(data.projects)}")

        if unresolved_authors:
            print(f"\nUnresolved authors ({len(unresolved_authors)}):")
            for name in sorted(unresolved_authors):
                print(f"  - {name}")

        if unknown_projects:
            print(f"\nUnknown project IDs ({len(unknown_projects)}):")
            for pid in sorted(unknown_projects):
                print(f"  - {pid}")
            errors += len(unknown_projects)

        if errors:
            print(f"\nValidation found {errors} error(s).")
            sys.exit(1)
        else:
            print("\nValidation passed.")
        return

    # --unresolved mode
    if args.unresolved:
        if not unresolved_authors:
            print("All authors resolved.")
        else:
            print(f"Unresolved authors ({len(unresolved_authors)}):")
            for name in sorted(unresolved_authors):
                print(f"  {name}")
        return

    # Export
    export_func = export_to_yaml if args.format == 'yaml' else export_to_json
    export_func(data, args.output)

    print(f"Wrote {args.output}")
    print(f"  {len(data.publications)} publications, "
          f"{len(data.people)} people, "
          f"{len(data.projects)} projects")


if __name__ == "__main__":
    main()
