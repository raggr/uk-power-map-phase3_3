# UK Government Power Map

A comprehensive political accountability and representation tool, built as a static web application.

## Project Status

| Phase | Name | Status |
|-------|------|--------|
| **0** | Project scaffold & data architecture | ✅ Complete |
| **1a** | MP ethnicity dataset | ⬜ Not started |
| **1b** | Constituency demographics | ⬜ Not started |
| **2** | Refactor app + diversity view | ⬜ Not started |
| **3** | Static choropleth maps | ⬜ Not started |
| **4** | Interactive in-app map (Leaflet) | ⬜ Not started |
| **5** | Issue badges: Palestine (votes) | ⬜ Not started |
| **6** | Issue badges: meetings data | ⬜ Not started |
| **7** | IfG historical timeline | ⬜ Not started |
| **8** | Polish & deployment | ⬜ Not started |

## Quick Start

```bash
# Serve locally (required for fetch() to work)
cd uk-power-map
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

## Project Structure

```
uk-power-map/
├── index.html                  ← Main app (loads data via fetch)
├── original-index.html         ← Original monolithic file (reference)
├── build.py                    ← Build pipeline
├── README.md
├── data/
│   ├── departments.json        ← Department structure + ministers
│   ├── cross-cutting.json      ← Cross-cutting & law officer roles
│   ├── lords-whips.json        ← House of Lords whips
│   ├── changelog.json          ← Recent changes log
│   ├── wealth-estimates.json   ← Minister wealth estimates
│   ├── mp-info.json            ← Per-MP: constituency, majority, parlId
│   ├── dept-budgets.json       ← Department budgets (Total DEL)
│   ├── wealth-percentile-thresholds.json  ← ONS wealth distribution
│   ├── sources/                ← Raw downloaded source files
│   └── issues/                 ← Issue-specific data (Phase 5+)
│       ├── palestine.json      ← (future)
│       └── arms-trade.json     ← (future)
├── maps/                       ← Static choropleth maps (Phase 3)
├── assets/                     ← Shared assets (GeoJSON, etc.)
└── scripts/
    └── extract_data.py         ← Extracts data from original HTML
```

## Data Architecture

All data is stored as separate JSON files loaded on demand via `fetch()`.
The key join field across datasets is `parlId` (MNIS parliamentary ID).

### Core data files (Phase 0)
- **departments.json**: 19 departments, each with secretary, MoS, and PUSS arrays
- **mp-info.json**: 102 entries with `{con, maj, parlId}` — the master lookup table
- **wealth-estimates.json**: Estimated wealth per minister
- **dept-budgets.json**: Total DEL 2025–26 per department

### Future data files
- **ethnicity-mps.json** (Phase 1a): Ethnic minority MP records
- **constituency-demographics.json** (Phase 1b): Census 2021 data per constituency
- **issues/*.json** (Phase 5+): Voting records, meetings, speeches per policy issue

## Build Pipeline

```bash
python build.py              # Full build
python build.py extract      # Re-extract data from original HTML
python build.py dist         # Copy deployable files to dist/
```

## Attribution

- Data: GOV.UK, Hansard, House of Commons Library
- Wealth: Published estimates + ONS Wealth and Assets Survey 2020–22
- Budgets: HM Treasury Main Estimates 2025–26
- Photos: members-api.parliament.uk
- Future: IfG Ministers Database (CC-BY-4.0), British Future, TheyWorkForYou (mySociety), ONS Census 2021
