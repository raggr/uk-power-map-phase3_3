#!/usr/bin/env python3
"""
Phase 0: Extract embedded JavaScript data from the original index.html
into separate JSON files for the refactored multi-file architecture.
"""

import json
import re
import os

SRC = "original-index.html"
DATA_DIR = "data"

with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# Extract the <script> block
script_match = re.search(r"<script>\s*// DATA\s*(.*?)\s*// WEALTH PERCENTILE", html, re.DOTALL)
if not script_match:
    raise ValueError("Could not find DATA section in HTML")

data_section = script_match.group(1)

# We also need WEALTH_EST and MP_INFO which are after DATA section
full_script = re.search(r"<script>(.*?)</script>", html, re.DOTALL).group(1)

# --- Strategy: use a JS-like parser approach ---
# Since the data is valid JS object literals, we can convert them to JSON
# by extracting each var block and doing careful regex transforms

def js_var_to_json(varname, source):
    """Extract a JS var assignment and convert to JSON-compatible string."""
    # Match: var VARNAME = [...]; or var VARNAME = {...};
    pattern = rf'var\s+{varname}\s*=\s*'
    match = re.search(pattern, source)
    if not match:
        raise ValueError(f"Could not find var {varname}")
    
    start = match.end()
    
    # Find the matching closing bracket/brace
    depth = 0
    i = start
    opener = source[i]
    if opener == '[':
        close = ']'
    elif opener == '{':
        close = '}'
    else:
        raise ValueError(f"Expected [ or {{ after var {varname}, got {opener}")
    
    while i < len(source):
        ch = source[i]
        if ch == opener:
            depth += 1
        elif ch == close:
            depth -= 1
            if depth == 0:
                break
        elif ch in ('"', "'"):
            # Skip string content
            quote = ch
            i += 1
            while i < len(source) and source[i] != quote:
                if source[i] == '\\':
                    i += 1  # skip escaped char
                i += 1
        i += 1
    
    raw = source[start:i+1]
    return raw


def js_to_json(raw):
    """Convert JS object/array literal to valid JSON."""
    s = raw
    # Replace single-quoted strings (careful not to break apostrophes inside doubles)
    # For our data, keys are unquoted identifiers — we need to quote them
    
    # Quote unquoted keys: word characters before colon
    s = re.sub(r'(?<=[{,\n])\s*(\w+)\s*:', r'"\1":', s)
    
    # Handle trailing commas before } or ]
    s = re.sub(r',\s*([}\]])', r'\1', s)
    
    # Replace JS true/false/null (already JSON compatible, but just in case)
    # Handle unicode escapes — these are already valid JSON
    
    # Handle single-quoted strings -> double-quoted
    # This is tricky; our data mostly uses double quotes already
    
    return s


def extract_and_save(varname, filename, source):
    """Extract a JS variable and save as JSON."""
    raw = js_var_to_json(varname, source)
    json_str = js_to_json(raw)
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        # Save the raw conversion for debugging
        debug_path = os.path.join(DATA_DIR, f"_debug_{filename}")
        with open(debug_path, "w") as f:
            f.write(json_str)
        print(f"  ERROR parsing {varname}: {e}")
        print(f"  Raw saved to {debug_path} for debugging")
        return None
    
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print stats
    if isinstance(data, list):
        print(f"  {varname} -> {filename}: {len(data)} items")
    elif isinstance(data, dict):
        print(f"  {varname} -> {filename}: {len(data)} keys")
    
    return data


print("Extracting data from original index.html...")
print()

departments = extract_and_save("DEPARTMENTS", "departments.json", full_script)
cross_cutting = extract_and_save("CROSS_CUTTING", "cross-cutting.json", full_script)
lords_whips = extract_and_save("LORDS_WHIPS", "lords-whips.json", full_script)
changelog = extract_and_save("CHANGELOG", "changelog.json", full_script)
wealth_est = extract_and_save("WEALTH_EST", "wealth-estimates.json", full_script)
mp_info = extract_and_save("MP_INFO", "mp-info.json", full_script)
dept_budget = extract_and_save("DEPT_BUDGET", "dept-budgets.json", full_script)

# Also extract the wealth percentile thresholds
wpt_match = re.search(r'var\s+WPT\s*=\s*(\[.*?\]);', full_script)
if wpt_match:
    wpt_data = json.loads(wpt_match.group(1))
    with open(os.path.join(DATA_DIR, "wealth-percentile-thresholds.json"), "w") as f:
        json.dump(wpt_data, f, indent=2)
    print(f"  WPT -> wealth-percentile-thresholds.json: {len(wpt_data)} thresholds")

print()
print("Done. Files saved to data/")
print()

# Verify key relationships
if mp_info and departments:
    all_ministers = set()
    for dept in departments:
        all_ministers.add(dept["secretary"]["name"])
        for m in dept.get("mos", []):
            all_ministers.add(m["name"])
        for m in dept.get("puss", []):
            all_ministers.add(m["name"])
    
    mp_names = set(mp_info.keys()) if mp_info else set()
    
    missing_from_mp_info = all_ministers - mp_names
    if missing_from_mp_info:
        print(f"WARNING: {len(missing_from_mp_info)} ministers not in MP_INFO:")
        for n in sorted(missing_from_mp_info):
            print(f"  - {n}")
    
    extra_in_mp_info = mp_names - all_ministers
    # These are expected (cross-cutting, whips, etc.)
    
    ministers_with_parlid = sum(1 for v in mp_info.values() if v.get("parlId"))
    print(f"Ministers with parlId: {ministers_with_parlid}/{len(mp_info)}")
    print(f"Total unique ministers in departments: {len(all_ministers)}")
