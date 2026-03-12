#!/usr/bin/env python3
"""
Process real data sources into ward-level RSI scores for Haringey.
All scores derived from verifiable public data — no placeholders.
v2: includes IMD and VOA via LSOA centroid → ward point-in-polygon.
"""
import json, csv, math
from shapely.geometry import Point, shape
from collections import defaultdict

# ============================================================
# 1. LOAD WARD BOUNDARIES
# ============================================================
with open('index.html', 'r') as f:
    content = f.read()
start = content.find('const wardsGeoJSON = ') + len('const wardsGeoJSON = ')
end = content.find(';\n', start)
geojson = json.loads(content[start:end])

ward_shapes = {}
for feature in geojson['features']:
    name = feature['properties']['name']
    ward_shapes[name] = shape(feature['geometry'])
print(f"Loaded {len(ward_shapes)} ward boundaries")

# ============================================================
# 2. LOAD LSOA CENTROIDS (from ONS ArcGIS)
# ============================================================
with open('lsoa_centroids_haringey.json', 'r') as f:
    lsoa_centroids = json.load(f)
print(f"Loaded {len(lsoa_centroids)} LSOA centroids")

# Map each LSOA to a ward via point-in-polygon
lsoa_to_ward = {}
unmapped = []
for lsoa_code, centroid in lsoa_centroids.items():
    pt = Point(centroid['lon'], centroid['lat'])
    found = False
    for ward_name, ward_shape in ward_shapes.items():
        if ward_shape.contains(pt):
            lsoa_to_ward[lsoa_code] = ward_name
            found = True
            break
    if not found:
        # Try with a buffer for edge cases
        for ward_name, ward_shape in ward_shapes.items():
            if ward_shape.buffer(0.001).contains(pt):
                lsoa_to_ward[lsoa_code] = ward_name
                found = True
                break
        if not found:
            unmapped.append(lsoa_code)

print(f"Mapped {len(lsoa_to_ward)}/{len(lsoa_centroids)} LSOAs to wards")
if unmapped:
    print(f"  Unmapped: {unmapped}")

# Show mapping counts per ward
ward_lsoa_counts = defaultdict(int)
for w in lsoa_to_ward.values():
    ward_lsoa_counts[w] += 1
for w in sorted(ward_lsoa_counts.keys()):
    print(f"  {w}: {ward_lsoa_counts[w]} LSOAs")

# ============================================================
# 3. IMD 2019 — LSOA-level, aggregate to wards
# ============================================================
print("\nAggregating IMD 2019 data to wards...")
imd_by_ward = defaultdict(lambda: {'total_weighted_score': 0, 'total_pop': 0})

with open('imd2019_file7.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Local Authority District code (2019)') != 'E09000014':
            continue
        lsoa_code = row['LSOA code (2011)']
        ward = lsoa_to_ward.get(lsoa_code)
        if not ward:
            continue
        try:
            # Use IMD overall score (not just Living Environment)
            imd_score = float(row['Index of Multiple Deprivation (IMD) Score'])
            pop = int(row['Total population: mid 2015 (excluding prisoners)'])
            imd_by_ward[ward]['total_weighted_score'] += imd_score * pop
            imd_by_ward[ward]['total_pop'] += pop
        except (ValueError, KeyError):
            pass

ward_imd_score = {}
for ward, data in imd_by_ward.items():
    if data['total_pop'] > 0:
        ward_imd_score[ward] = data['total_weighted_score'] / data['total_pop']

print("IMD 2019 (population-weighted average) by ward:")
for w in sorted(ward_imd_score, key=lambda x: ward_imd_score[x], reverse=True):
    print(f"  {w}: {ward_imd_score[w]:.1f}")

# ============================================================
# 4. VOA COMMERCIAL PREMISES — LSOA-level, aggregate to wards
# ============================================================
print("\nAggregating VOA data to wards...")
voa_by_lsoa = {}

# The VOA file structure may vary — let's detect it
with open('voa_stock_2023/table_SOP_OA1_1.csv', 'r', encoding='latin-1') as f:
    reader = csv.reader(f)
    header_row = None
    for i, row in enumerate(reader):
        if i < 5:
            print(f"  Row {i}: {row[:5]}")
        if any('LSOA' in str(cell) for cell in row):
            header_row = i
            print(f"  Header found at row {i}: {row[:6]}")
            break

# Re-read with proper header handling
with open('voa_stock_2023/table_SOP_OA1_1.csv', 'r', encoding='latin-1') as f:
    reader = csv.reader(f)
    rows = list(reader)

if header_row is not None:
    headers = rows[header_row]
    data_rows = rows[header_row + 1:]
else:
    headers = rows[0]
    data_rows = rows[1:]

print(f"  Headers: {headers[:8]}")

# Find column indices
lsoa_col = None
total_col = None
for i, h in enumerate(headers):
    h_lower = str(h).lower()
    if 'lsoa' in h_lower and 'code' in h_lower:
        lsoa_col = i
    elif h_lower.strip() == 'total' or 'total' in h_lower:
        if total_col is None:
            total_col = i

print(f"  LSOA col: {lsoa_col}, Total col: {total_col}")

if lsoa_col is not None and total_col is not None:
    for row in data_rows:
        if len(row) > max(lsoa_col, total_col):
            lsoa_code = row[lsoa_col].strip()
            if lsoa_code in lsoa_to_ward:
                try:
                    total = int(row[total_col].replace(',', '').strip())
                    voa_by_lsoa[lsoa_code] = total
                except (ValueError, IndexError):
                    pass

# Aggregate to wards
voa_by_ward = defaultdict(int)
for lsoa_code, count in voa_by_lsoa.items():
    ward = lsoa_to_ward.get(lsoa_code)
    if ward:
        voa_by_ward[ward] += count

if voa_by_ward:
    print(f"VOA commercial premises by ward:")
    for w in sorted(voa_by_ward, key=lambda x: voa_by_ward[x], reverse=True):
        print(f"  {w}: {voa_by_ward[w]}")
else:
    print("  No VOA data mapped to wards (may need different column parsing)")

# ============================================================
# 5. FSA FOOD ESTABLISHMENTS — point-in-polygon
# ============================================================
print("\nProcessing FSA data...")
with open('fsa_haringey.json', 'r') as f:
    fsa_data = json.load(f)
establishments = fsa_data if isinstance(fsa_data, list) else fsa_data.get('establishments', [])

food_outlet_counts = defaultdict(int)
takeaway_counts = defaultdict(int)

for est in establishments:
    lat = est.get('geocode', {}).get('latitude')
    lon = est.get('geocode', {}).get('longitude')
    btype = est.get('BusinessType', '')
    if lat and lon:
        try:
            pt = Point(float(lon), float(lat))
            for ward_name, ward_shape in ward_shapes.items():
                if ward_shape.contains(pt):
                    food_outlet_counts[ward_name] += 1
                    if 'takeaway' in btype.lower() or 'sandwich' in btype.lower():
                        takeaway_counts[ward_name] += 1
                    break
        except (ValueError, TypeError):
            pass

# ============================================================
# 6. CENSUS 2021 DATA
# ============================================================
census_population = {
    "Alexandra Park": 8839, "Bounds Green": 9833, "Bruce Castle": 13477,
    "Crouch End": 13040, "Fortis Green": 12598, "Harringay": 14567,
    "Hermitage & Gardens": 8437, "Highgate": 12764, "Hornsey": 15035,
    "Muswell Hill": 8779, "Noel Park": 13712, "Northumberland Park": 14705,
    "Seven Sisters": 9238, "South Tottenham": 16821, "St Ann's": 10590,
    "Stroud Green": 10792, "Tottenham Central": 14739, "Tottenham Hale": 12176,
    "West Green": 14968, "White Hart Lane": 13882, "Woodside": 15245,
}

census_pct_flats = {
    "Alexandra Park": 42.5, "Bounds Green": 61.2, "Bruce Castle": 63.5,
    "Crouch End": 70.6, "Fortis Green": 45.0, "Harringay": 63.7,
    "Hermitage & Gardens": 56.3, "Highgate": 62.2, "Hornsey": 66.5,
    "Muswell Hill": 58.8, "Noel Park": 51.1, "Northumberland Park": 63.9,
    "Seven Sisters": 57.9, "South Tottenham": 57.4, "St Ann's": 55.1,
    "Stroud Green": 74.5, "Tottenham Central": 54.6, "Tottenham Hale": 58.0,
    "West Green": 54.1, "White Hart Lane": 25.8, "Woodside": 66.1,
}

# Ward areas from GeoJSON
def polygon_area_hectares(poly):
    coords = list(poly.exterior.coords)
    lat_mid = sum(c[1] for c in coords) / len(coords)
    m_per_deg_lat = 111320.0
    m_per_deg_lon = 111320.0 * math.cos(math.radians(lat_mid))
    n = len(coords)
    area_sq_m = 0.0
    for i in range(n):
        j = (i + 1) % n
        x1, y1 = coords[i][0] * m_per_deg_lon, coords[i][1] * m_per_deg_lat
        x2, y2 = coords[j][0] * m_per_deg_lon, coords[j][1] * m_per_deg_lat
        area_sq_m += x1 * y2 - x2 * y1
    return abs(area_sq_m) / 2.0 / 10000.0

ward_areas = {name: polygon_area_hectares(shp) for name, shp in ward_shapes.items()}
pop_density = {w: census_population[w] / ward_areas[w] for w in census_population if ward_areas.get(w, 0) > 0}

# ============================================================
# 7. FIXMYSTREET
# ============================================================
fixmystreet_counts = {
    "Alexandra Park": 40, "Bounds Green": 282, "Bruce Castle": 52,
    "Crouch End": 25, "Fortis Green": 119, "Harringay": 132,
    "Hermitage & Gardens": 127, "Highgate": 185, "Hornsey": 51,
    "Muswell Hill": 79, "Noel Park": 255, "Northumberland Park": 55,
    "Seven Sisters": 79, "South Tottenham": 85, "St Ann's": 63,
    "Stroud Green": 52, "Tottenham Central": 142, "Tottenham Hale": 58,
    "West Green": 125, "White Hart Lane": 59, "Woodside": 183,
}
fixmystreet_per_1k = {w: (fixmystreet_counts[w] / census_population[w]) * 1000 for w in fixmystreet_counts}

# ============================================================
# 8. TfL STATION USAGE
# ============================================================
station_usage = {
    "Alexandra Park": 1_595_988, "Bounds Green": 4_266_560,
    "Bruce Castle": 3_961_943, "Crouch End": 0, "Fortis Green": 0,
    "Harringay": 2_909_438, "Hermitage & Gardens": 0, "Highgate": 4_408_040,
    "Hornsey": 1_500_360, "Muswell Hill": 0, "Noel Park": 7_948_900,
    "Northumberland Park": 943_776, "Seven Sisters": 19_728_156,
    "South Tottenham": 4_709_543, "St Ann's": 0, "Stroud Green": 2_006_957,
    "Tottenham Central": 0, "Tottenham Hale": 21_738_093, "West Green": 0,
    "White Hart Lane": 4_491_024, "Woodside": 9_088_053,
}

# ============================================================
# 9. NORMALISE AND CALCULATE RSI
# ============================================================
wards = sorted(ward_shapes.keys())

def min_max_normalise(values_dict):
    vals = [values_dict.get(w, 0) for w in wards]
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return {w: 5.0 for w in wards}
    return {w: round(((values_dict.get(w, 0) - mn) / (mx - mn)) * 10, 1) for w in wards}

# Compute per-capita metrics
food_per_1k = {w: (food_outlet_counts.get(w, 0) / census_population.get(w, 1)) * 1000 for w in wards}

# Fill missing IMD/VOA with 0 for wards not covered
for w in wards:
    if w not in ward_imd_score:
        ward_imd_score[w] = 0
    if w not in voa_by_ward:
        voa_by_ward[w] = 0

# Commercial premises per hectare
commercial_per_ha = {w: voa_by_ward.get(w, 0) / ward_areas.get(w, 1) for w in wards}

# Indicator definitions
raw_indicators = {
    'fixmystreet': fixmystreet_per_1k,
    'food_outlets': food_per_1k,
    'imd': ward_imd_score,
    'pct_flats': census_pct_flats,
    'pop_density': pop_density,
    'station_usage': station_usage,
    'commercial': commercial_per_ha if any(v > 0 for v in voa_by_ward.values()) else None,
}

# Remove None indicators
raw_indicators = {k: v for k, v in raw_indicators.items() if v is not None}

normalised = {}
for key, raw in raw_indicators.items():
    normalised[key] = min_max_normalise(raw)

# Weights — revised for 6 or 7 indicators
if 'commercial' in raw_indicators:
    weights = {
        'fixmystreet': 0.20,
        'food_outlets': 0.15,
        'imd': 0.20,
        'pct_flats': 0.10,
        'pop_density': 0.15,
        'station_usage': 0.10,
        'commercial': 0.10,
    }
else:
    weights = {
        'fixmystreet': 0.20,
        'food_outlets': 0.15,
        'imd': 0.25,
        'pct_flats': 0.10,
        'pop_density': 0.15,
        'station_usage': 0.15,
    }

print(f"\nWeights: {weights}")
print(f"Sum: {sum(weights.values())}")

# Calculate RSI
rsi_scores = {}
for w in wards:
    rsi = sum(normalised[ind].get(w, 0) * wt for ind, wt in weights.items())
    rsi_scores[w] = round(rsi, 1)

print("\n" + "="*60)
print("COMPOSITE RSI SCORES")
print("="*60)
for w in sorted(wards, key=lambda x: rsi_scores[x], reverse=True):
    parts = " + ".join(f"{ind}:{normalised[ind].get(w,0):.0f}×{wt}" for ind, wt in weights.items())
    print(f"  {w}: {rsi_scores[w]:.1f}")

# ============================================================
# 10. OUTPUT JAVASCRIPT
# ============================================================
indicator_labels = {
    'fixmystreet': 'FixMyStreet reports',
    'food_outlets': 'Food outlet density',
    'imd': 'IMD deprivation score',
    'pct_flats': '% flats (Census 2021)',
    'pop_density': 'Population density',
    'station_usage': 'Station usage (TfL/NR)',
    'commercial': 'Commercial premises density',
}

tier_labels = {
    'fixmystreet': 'T1',
    'food_outlets': 'T1',
    'imd': 'T1',
    'pct_flats': 'T2',
    'pop_density': 'T2',
    'station_usage': 'T2',
    'commercial': 'T1',
}

kbt_notes = {
    "Alexandra Park": "Among the best wards surveyed. Detritus was the main issue, with leaf fall contributing to problems on residential roads.",
    "Crouch End": "Leaf fall heavy. Retail areas acceptable for litter but residential roads off retail areas heavily affected.",
    "Fortis Green": "Litter better than other areas surveyed. Graffiti observed on utility boxes and alleyway walls.",
    "Harringay": "Serious detritus on Ladder streets. Fly-tipping observed near Haringey Passage.",
    "Highgate": "Detritus was the main issue. Leaf fall not cleared, causing related drainage and slip problems.",
    "Noel Park": "Heavy litter on side streets off the high street. KBT noted \\u2018considerably different frequencies of cleansing\\u2019 as the cause of variation between main retail area and surrounding streets.",
    "Northumberland Park": "Among the least favourable of all wards for every element surveyed. Massive fly-tips observed. Leeside Road had \\u2018one of the most significant fly-tips the surveyor had ever seen.\\u2019 Industrial areas severely affected.",
    "Bruce Castle": "Litter and graffiti prevalent on footpaths. Vandalised utility boxes observed throughout the ward.",
    "Tottenham Hale": "Residential areas near the High Road had serious litter issues. Fly-tipping around Roseberry Avenue and Carbuncle Passage.",
    "Woodside": "Among the best for litter and detritus. Graffiti was a serious issue in industrial areas.",
}

# Build raw value strings
def get_raw_str(ind_key, ward):
    if ind_key == 'fixmystreet':
        return f"{fixmystreet_per_1k[ward]:.1f} per 1k residents ({fixmystreet_counts[ward]} total)"
    elif ind_key == 'food_outlets':
        return f"{food_per_1k[ward]:.1f} per 1k residents ({food_outlet_counts.get(ward, 0)} outlets)"
    elif ind_key == 'imd':
        return f"{ward_imd_score.get(ward, 0):.1f} (pop-weighted avg)"
    elif ind_key == 'pct_flats':
        return f"{census_pct_flats[ward]:.1f}%"
    elif ind_key == 'pop_density':
        return f"{pop_density.get(ward, 0):.0f} persons/ha"
    elif ind_key == 'station_usage':
        v = station_usage.get(ward, 0)
        return f"{v:,} annual entries+exits" if v > 0 else "No station in ward"
    elif ind_key == 'commercial':
        return f"{commercial_per_ha.get(ward, 0):.1f} per hectare ({voa_by_ward.get(ward, 0)} total)"
    return ""

lines = ['const wardData = {']
for w in wards:
    kbt = kbt_notes.get(w)
    kbt_js = json.dumps(kbt) if kbt else 'null'
    lines.append(f'  "{w}": {{')
    lines.append(f'    rsi: {rsi_scores[w]},')
    lines.append(f'    indicators: {{')
    for ind_key in weights:
        label = indicator_labels[ind_key]
        score = normalised[ind_key].get(w, 0)
        raw = get_raw_str(ind_key, w)
        lines.append(f'      {ind_key}: {{ score: {score}, label: "{label}", raw: "{raw}" }},')
    lines.append(f'    }},')
    lines.append(f'    kbt: {kbt_js}')
    lines.append(f'  }},')
lines.append('};')

# Weights JS
lines.append('')
lines.append('const weights = {')
for k, v in weights.items():
    lines.append(f'  {k}: {v},')
lines.append('};')

# Tier labels
lines.append('')
lines.append('const tierLabels = {')
for k in weights:
    lines.append(f'  {k}: "{tier_labels.get(k, "T2")}",')
lines.append('};')

js_output = '\n'.join(lines)
with open('ward_data_real.js', 'w') as f:
    f.write(js_output)
print(f"\nJavaScript written to ward_data_real.js")

# Summary
print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"  Wards: {len(wards)}")
print(f"  Indicators: {len(weights)}")
print(f"  RSI range: {min(rsi_scores.values())} - {max(rsi_scores.values())}")
print(f"  Mean RSI: {sum(rsi_scores.values())/len(rsi_scores):.1f}")
print(f"  Highest: {max(rsi_scores, key=lambda x: rsi_scores[x])} ({max(rsi_scores.values())})")
print(f"  Lowest: {min(rsi_scores, key=lambda x: rsi_scores[x])} ({min(rsi_scores.values())})")
