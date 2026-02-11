#!/usr/bin/env python3
"""
UK Government Power Map — Build Pipeline

Runs all data processing steps and outputs deployable files to dist/.

Usage:
    python build.py              # Full build
    python build.py extract      # Phase 0: Extract data from original HTML
    python build.py ethnicity    # Phase 1a: Process MP ethnicity data
    python build.py demographics # Phase 1b: Process constituency demographics
    python build.py maps         # Phase 3: Generate static choropleth maps
    python build.py issues       # Phase 5-6: Process issue/voting data
    python build.py timeline     # Phase 7: Process IfG historical data
"""

import sys
import os
import json
import shutil

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SOURCES_DIR = os.path.join(DATA_DIR, "sources")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")
MAPS_DIR = os.path.join(PROJECT_ROOT, "maps")


def ensure_dirs():
    """Create all required directories."""
    for d in [DATA_DIR, SOURCES_DIR, DIST_DIR, MAPS_DIR,
              os.path.join(DATA_DIR, "issues")]:
        os.makedirs(d, exist_ok=True)


def phase_0_extract():
    """Extract data from the original monolithic HTML file."""
    print("=== Phase 0: Extract data from original HTML ===")
    os.system(f"cd {PROJECT_ROOT} && python3 scripts/extract_data.py")


def phase_1a_ethnicity():
    """Process MP ethnicity data."""
    print("=== Phase 1a: MP ethnicity data ===")
    # TODO: Phase 1a
    # - Load data/sources/british-future-2024.json (manually curated)
    # - Cross-reference with data/mp-info.json parlIds
    # - Output data/ethnicity-mps.json
    print("  Not yet implemented. See execution plan Phase 1a.")


def phase_1b_demographics():
    """Process constituency demographics from Census 2021."""
    print("=== Phase 1b: Constituency demographics ===")
    # TODO: Phase 1b
    # - Download/load Census TS021 at constituency level
    # - Map to 2024 boundaries
    # - Fuzzy-match constituency names to MP_INFO
    # - Output data/constituency-demographics.json
    print("  Not yet implemented. See execution plan Phase 1b.")


def phase_3_maps():
    """Generate static choropleth maps."""
    print("=== Phase 3: Static choropleth maps ===")
    # TODO: Phase 3
    # - Load constituency GeoJSON + demographics
    # - Generate PNG/SVG maps with GeoPandas + Matplotlib
    # - Output to maps/
    print("  Not yet implemented. See execution plan Phase 3.")


def phase_5_issues():
    """Process issue badge data (votes, meetings)."""
    print("=== Phase 5-6: Issue badge data ===")
    # TODO: Phase 5-6
    # - Load TheyWorkForYou voting data
    # - Process ministerial meetings CSVs
    # - Output data/issues/palestine.json, data/issues/arms-trade.json, etc.
    print("  Not yet implemented. See execution plan Phases 5-6.")


def phase_7_timeline():
    """Process IfG Ministers Database for historical timeline."""
    print("=== Phase 7: Historical timeline ===")
    # TODO: Phase 7
    # - Download IfG Ministers Database from GitHub
    # - Process appointments, link to ethnicity data
    # - Output data/ifg-appointments.json
    print("  Not yet implemented. See execution plan Phase 7.")


def build_dist():
    """Copy all deployable files to dist/."""
    print("=== Building dist/ ===")
    ensure_dirs()
    
    # Copy main HTML
    shutil.copy2(os.path.join(PROJECT_ROOT, "index.html"),
                 os.path.join(DIST_DIR, "index.html"))
    
    # Copy data files
    dist_data = os.path.join(DIST_DIR, "data")
    if os.path.exists(dist_data):
        shutil.rmtree(dist_data)
    shutil.copytree(DATA_DIR, dist_data,
                    ignore=shutil.ignore_patterns("sources", "_debug_*"))
    
    # Copy maps if they exist
    dist_maps = os.path.join(DIST_DIR, "maps")
    if os.path.exists(MAPS_DIR) and os.listdir(MAPS_DIR):
        if os.path.exists(dist_maps):
            shutil.rmtree(dist_maps)
        shutil.copytree(MAPS_DIR, dist_maps)
    
    print(f"  dist/ built with {sum(len(f) for _, _, f in os.walk(DIST_DIR))} files")


COMMANDS = {
    "extract": phase_0_extract,
    "ethnicity": phase_1a_ethnicity,
    "demographics": phase_1b_demographics,
    "maps": phase_3_maps,
    "issues": phase_5_issues,
    "timeline": phase_7_timeline,
    "dist": build_dist,
}


def main():
    ensure_dirs()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd in COMMANDS:
            COMMANDS[cmd]()
        else:
            print(f"Unknown command: {cmd}")
            print(f"Available: {', '.join(COMMANDS.keys())}")
            sys.exit(1)
    else:
        # Full build
        phase_0_extract()
        phase_1a_ethnicity()
        phase_1b_demographics()
        phase_3_maps()
        phase_5_issues()
        phase_7_timeline()
        build_dist()
    
    print("\nDone.")


if __name__ == "__main__":
    main()
