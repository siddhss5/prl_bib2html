"""
Command-line interface for labdata.

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import argparse
import sys
from pathlib import Path

from .config_schema import LibraryConfig
from .publications import list_publications, load_projects_config, list_publications_by_project
from .exporters import publications_to_dict, projects_to_dict, export_to_yaml, export_to_json


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate publication data from BibTeX files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate YAML output
  labdata --config config.yaml --format yaml --output publications.yml

  # Generate JSON output
  labdata --config config.yaml --format json --output publications.json

  # Generate both publications and projects
  labdata --config config.yaml --format yaml --output-dir _data/
        """
    )
    
    parser.add_argument(
        '--config',
        required=True,
        help='Path to YAML configuration file'
    )
    
    parser.add_argument(
        '--format',
        choices=['yaml', 'json'],
        default='yaml',
        help='Output format (default: yaml)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (e.g., publications.yml)'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for publications.yml and projects.yml (alternative to --output)'
    )
    
    parser.add_argument(
        '--projects-only',
        action='store_true',
        help='Generate only projects data'
    )
    
    parser.add_argument(
        '--publications-only',
        action='store_true',
        help='Generate only publications data'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.output and not args.output_dir:
        parser.error("Either --output or --output-dir must be specified")
    
    if args.output and args.output_dir:
        parser.error("Cannot specify both --output and --output-dir")
    
    # Load configuration
    try:
        config = LibraryConfig.from_yaml(args.config)
        legacy_config = config.to_publications_config()
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {args.config}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Determine export function
    export_func = export_to_yaml if args.format == 'yaml' else export_to_json
    file_ext = 'yml' if args.format == 'yaml' else 'json'
    
    # Generate publications
    if not args.projects_only:
        print("📚 Generating publications data...")
        pubs = list_publications(legacy_config)
        pubs_dict = publications_to_dict(pubs)
        
        if args.output:
            output_path = args.output
        else:
            output_path = str(Path(args.output_dir) / f"publications.{file_ext}")
        
        export_func(pubs_dict, output_path)
        
        total_pubs = sum(len(p) for year in pubs_dict.values() for p in year.values())
        print(f"✅ Generated: {output_path}")
        print(f"   Found {total_pubs} publications across {len(pubs_dict)} years")
    
    # Generate projects
    if not args.publications_only and legacy_config.projects_yaml_path:
        print("\n📁 Generating projects data...")
        projects_config = load_projects_config(legacy_config.projects_yaml_path)
        
        if not projects_config:
            print("⚠️  No projects configured")
        else:
            project_pubs = list_publications_by_project(legacy_config, projects_config)
            
            # Sort projects
            def project_sort_key(item):
                project_name, project_info = item
                status = project_info.get('status', '').lower()
                status_priority = {'active': 0, 'archived': 1}.get(status, 2)
                newest_year = 0
                if project_name in project_pubs and project_pubs[project_name]:
                    newest_year = max(pub.year for pub in project_pubs[project_name])
                return (status_priority, -newest_year, project_name)
            
            sorted_projects = dict(sorted(projects_config.items(), key=project_sort_key))
            projects_dict = projects_to_dict(sorted_projects, project_pubs)
            
            if args.output_dir:
                output_path = str(Path(args.output_dir) / f"projects.{file_ext}")
            else:
                # If using --output, derive projects filename
                output_path = str(Path(args.output).parent / f"projects.{file_ext}")
            
            export_func(projects_dict, output_path)
            
            total_project_pubs = sum(len(p['publications']) for p in projects_dict.values())
            print(f"✅ Generated: {output_path}")
            print(f"   Found {len(projects_dict)} projects with {total_project_pubs} publications")
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()

