# UK Government Power Map — Project Journal
## Last updated: 2026-02-11

---

## PHASE STATUS

| Phase | Status | Description |
|-------|--------|-------------|
| 0 | ✅ | Refactored monolithic HTML to multi-file architecture |
| 1a | ✅ | MP ethnicity dataset (ministers only, n=17) |
| 1b | ✅ | Constituency demographics (650 seats, Census 2021) |
| 2 | ✅ | Diversity view UI in main index.html |
| 3 | ✅ | Interactive Leaflet.js maps — original 5 layers |
| 3.1 | ✅ | Expanded to all 87 minority MPs (from 17 ministers) |
| 3.2 | 🔧 IN PROGRESS | Replacing crude "Representation Gap" layer with analytically rigorous alternatives informed by Campbell & Heath (2021) |

---

## CURRENT FILE STRUCTURE

```
uk-power-map/
├── index.html              (42KB — main org chart with diversity view)
├── maps/index.html         (14KB — Leaflet.js interactive maps)
├── assets/
│   ├── constituencies.geojson  (8.8MB — 650 2024 boundaries, simplified)
│   └── map-data.json           (96KB — all 649 MPs with demographics)
├── data/
│   ├── departments.json
│   ├── cross-cutting.json
│   ├── mp-info.json
│   ├── ethnicity-mps.json         (ministers only, n=17)
│   ├── ethnicity-all-mps.json     (all minority MPs, n=87)
│   ├── constituency-demographics.json  (Census 2021)
│   ├── changelog.json
│   ├── dept-budgets.json
│   ├── wealth-estimates.json
│   └── lords-whips.json
├── scripts/
│   ├── extract_data.py
│   └── process_demographics.py
├── build.py
└── README.md
```

---

## MAP DATA STRUCTURE (assets/map-data.json)

Keyed by GSS code (PCON24CD). Each entry:
```json
{
  "name": "constituency name",
  "nw": 44.8,    // % non-White (Census 2021)
  "w": 55.2,     // % White
  "a": 10.3,     // % Asian
  "b": 19.3,     // % Black
  "mx": 6.2,     // % Mixed
  "o": 9.0,      // % Other
  "mp": "Name",
  "party": "Labour",
  "eth": "Black",           // broad ethnicity (only if minority MP)
  "ethd": "Black British",  // detail ethnicity
  "minister": {             // only if minister
    "name": "...", "rank": "...", "dept": "..."
  }
}
```

After Phase 3.2 rebuild, entries will also include:
- `leave`: Leave vote % (2016 referendum, Hanretty estimates, ~500 seats)
- `reform`: Reform UK vote share % (2024 election, full coverage)
- `winner`: winning party code (2024)
- `turnout`: turnout % (2024)
- `majority`: majority % (2024)
- `con`/`lab`/`ld`/`grn`: party vote shares (2024)

---

## CAMPBELL & HEATH (2021) — KEY INSIGHTS FOR THE PROJECT

### Paper: "Fueling the Populist Divide: Nativist and Cosmopolitan Preferences for Representation at the Elite and Mass Level"
Published in Political Behavior, 43:1707–1729. Uses BES 2015 Wave 6 (n=7490 voters) and Representative Audit of Britain (n=952 candidates).

### Core findings relevant to our maps:

1. **Representation preferences are ideological, not just demographic.** People don't simply want "more people like me" in parliament. They hold broader orientations: cosmopolitan (wanting diversity across all groups) vs nativist (wanting more local/working-class MPs, fewer ethnic minorities and Muslims).

2. **The elite-mass gap is the real story.** 80% of candidates hold cosmopolitan preferences vs 47% of voters. 22% of voters hold nativist preferences vs only 5% of candidates. This gap exists WITHIN every party (largest for Conservatives and UKIP).

3. **Nativist voters are politically alienated.** They are more likely to agree "politicians don't care what people like me think" and were more likely to support Brexit (70% Leave vs 25% for cosmopolitans).

4. **Leave vote is a validated proxy.** The paper finds nativist representation preferences strongly predict Brexit support even after controlling for demographics, partisanship, left-right scale, and attitudes to immigration.

5. **Working-class representation has collapsed** alongside rising ethnic/gender diversity — from 40% of Labour MPs being working class in 1951 to <10% by 2017. This creates a perceived zero-sum framing even though it needn't be.

6. **Party matters.** Voters choose parties, not individual candidates. The representation gap runs through party systems, not through individual constituency demographics.

### What this means for our crude "Representation Gap" map:

The old formula `(% non-White) - (minority MP × 100)` was a demographic mirror that implies every diverse constituency "should" have a minority MP. This is analytically hollow because:
- It ignores party selection mechanisms
- It ignores voter choice (people vote for parties)
- It treats MP ethnicity as the only dimension of representation
- It assumes representation is about demographic matching, which is exactly the simplistic view Campbell & Heath challenge
- It says nothing about whether voters actually WANT more diverse representation

---

## DATA ANALYSIS FINDINGS (from exploration of uploaded datasets)

### Datasets available:
1. **Brexit referendum estimates** — Hanretty constituency-level Leave % (2011 boundaries, 632 GB constituencies). Matched to 500 of 649 2024-boundary constituencies via word-overlap matching (77% coverage). NI excluded (no constituency-level data).
2. **2024 General Election results** — HoC Library data. Full 650 constituencies. Party votes, shares, turnout, majority.
3. **Census 2021 demographics** — already integrated (650 constituencies).
4. **87 ethnic minority MPs** — already integrated.

### Key correlations (n=500 complete cases):
- Leave% vs non-White%: r = -0.309 (moderate negative)
- Reform% vs non-White%: r = -0.360 (moderate negative)
- Reform% vs Leave%: r = 0.776 (strong positive — Reform vote maps closely onto the nativist dimension)

### Constituency typologies:
- **Cosmopolitan heartlands** (Leave<40%, non-White>20%): 37 seats. 41% have minority MPs.
- **Nativist pressure seats** (Leave>60%, Reform>20%, non-White<10%): 61 seats. 8% have minority MPs (5 total). Winners: Lab 38, Con 19, RUK 4.
- **Tension seats** (Leave>50%, non-White>20%): 62 seats. 29% have minority MPs.

### Within-party analysis (Labour seats, n=332):
- Low Leave third: 20.9% minority MPs, 25.7% non-White, 8.1% Reform
- Mid Leave third: 14.5% minority MPs, 17.6% non-White, 15.8% Reform
- High Leave third: 10.7% minority MPs, 13.9% non-White, 20.9% Reform

### Strong signal constituencies:
- **Strong nativist signal** (Leave>55%, Reform>20%): 113 seats, 10.6% minority MPs, 10.3% non-White
- **Strong cosmopolitan signal** (Leave<45%, Reform<10%): 98 seats, 21.4% minority MPs, 25.2% non-White

### Reform UK 2024:
- National mean: 14.4%, range 0.0–46.2%, median 14.9%
- 5 seats won outright
- Strongest in low-diversity, high-Leave constituencies — exactly the Campbell & Heath prediction

---

## PLAN FOR PHASE 3.2: NEW MAP LAYERS

### Keeping:
1. **Ethnic Diversity** (Census 2021 choropleth) — analytically sound, full coverage
2. **Minority MP Seats** (87 MPs colour-coded by broad ethnicity) — defensible at n=87

### Adding:
3. **Populist Mobilisation** (Reform UK 2024 vote share) — PRIMARY new layer
   - Sequential colour scale from low (pale) to high (dark red/purple)
   - Full 650-constituency coverage, 2024 data on 2024 boundaries
   - Directly measures where nativist populist sentiment translated into votes
   - Hover shows: Reform %, Leave % (where available), non-White %, MP details
   - This is the OUTCOME Campbell & Heath predicted from their representation gap framework

4. **Representation Terrain** (two-dimensional quadrant overlay) — ANALYTICAL layer
   - Combines ethnic diversity (Census) + voter orientation (Leave% or Reform%)
   - Four quadrant classification:
     - Cosmopolitan heartlands: low Leave/Reform, high diversity
     - Nativist pressure seats: high Leave/Reform, low diversity
     - Tension seats: high Leave/Reform AND high diversity
     - Middle ground: everything else
   - Colour-coded by quadrant with distinctive palettes
   - Available for ~500 constituencies (those with Brexit data)
   - This operationalises Campbell & Heath's core insight about competing visions of representation

### Removing:
- Old "Representation Gap" layer (crude demographic mirror)
- Old "Minister Seats" and "Seniority + Diversity" layers (already removed in 3.1)

### Implementation approach:
- Rebuild `assets/map-data.json` to include election + Brexit data per constituency
- Rebuild `maps/index.html` with 4 layers (Diversity, Minority MPs, Populist Mobilisation, Representation Terrain)
- Update hover panels to show richer multi-dimensional data
- Update legends and stats bars for new layers

---

## DATA SOURCES & ATTRIBUTION

| Dataset | Source | Coverage |
|---------|--------|----------|
| 2024 constituency boundaries | ONS / OS | 650 GeoJSON features |
| Census 2021 ethnic composition | ONS TS021, mapped to 2024 boundaries | 650 constituencies |
| Ethnic minority MPs | British Future 2024, HoC Library SN01156, Wikipedia | 87 MPs (all need verification) |
| All MPs | TheyWorkForYou | 649 (excl. Speaker) |
| Ministers | gov.uk, Parliament API | ~95 ministers |
| 2024 election results | House of Commons Library | 650 constituencies |
| EU referendum Leave estimates | Chris Hanretty (2017), areal interpolation | 632 GB constituencies (2011 boundaries), ~500 matched to 2024 |

---

## ANALYTICAL CAVEATS

1. **Ethnicity classifications** — all 87 minority MP classifications are based on secondary sources and flagged for verification. No self-identification data systematically collected.
2. **Brexit boundary matching** — 2016 Leave % estimates use 2011 constituency boundaries. ~77% matched to 2024 boundaries via word-overlap; remaining ~23% (mostly boundary-changed seats and NI) have no Leave data.
3. **Reform vote as nativist proxy** — while correlating at r=0.78 with Leave vote, Reform support reflects multiple factors beyond representation concerns.
4. **Working-class representation** — we lack systematic occupational background data for all 650 MPs. This is the biggest gap in operationalising the full Campbell & Heath framework.
5. **Gorton and Denton** — 1 of 650 constituencies has no MP data (vacant seat at time of TWFY data collection).
