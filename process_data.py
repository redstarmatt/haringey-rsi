#!/usr/bin/env python3
"""
Process real data sources into ward-level RSI scores for Haringey.
All scores derived from verifiable public data — no placeholders.
"""
import json, csv, math
from shapely.geometry import Point, shape
from collections import defaultdict

# ============================================================
# 1. LOAD WARD BOUNDARIES (from the inline GeoJSON in index.html)
# ============================================================
# Extract the GeoJSON by reading the HTML and finding the const
with open('index.html', 'r') as f:
    content = f.read()

start = content.find('const wardsGeoJSON = ') + len('const wardsGeoJSON = ')
# Find the end - it's a semicolon followed by newline
end = content.find(';\n', start)
geojson_str = content[start:end]
geojson = json.loads(geojson_str)

ward_shapes = {}
for feature in geojson['features']:
    name = feature['properties']['name']
    ward_shapes[name] = shape(feature['geometry'])

print(f"Loaded {len(ward_shapes)} ward boundaries")

# ============================================================
# 2. FSA FOOD ESTABLISHMENTS — point-in-polygon
# ============================================================
with open('fsa_haringey.json', 'r') as f:
    fsa_data = json.load(f)

establishments = fsa_data if isinstance(fsa_data, list) else fsa_data.get('establishments', [])
print(f"Processing {len(establishments)} FSA establishments...")

# Count food outlets per ward (focus on takeaway/food-on-the-go types)
food_outlet_counts = defaultdict(int)  # all food businesses
takeaway_counts = defaultdict(int)     # takeaway/sandwich shops specifically

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

print("\nFSA Food Outlets per ward:")
for w in sorted(food_outlet_counts.keys()):
    print(f"  {w}: {food_outlet_counts[w]} total, {takeaway_counts[w]} takeaway")

# ============================================================
# 3. CENSUS 2021 DATA (from research agent results)
# ============================================================
# Population data (Census 2021)
census_population = {
    "Alexandra Park": 8839,
    "Bounds Green": 9833,
    "Bruce Castle": 13477,
    "Crouch End": 13040,
    "Fortis Green": 12598,
    "Harringay": 14567,
    "Hermitage & Gardens": 8437,
    "Highgate": 12764,
    "Hornsey": 15035,
    "Muswell Hill": 8779,
    "Noel Park": 13712,
    "Northumberland Park": 14705,
    "Seven Sisters": 9238,
    "South Tottenham": 16821,
    "St Ann's": 10590,
    "Stroud Green": 10792,
    "Tottenham Central": 14739,
    "Tottenham Hale": 12176,
    "West Green": 14968,
    "White Hart Lane": 13882,
    "Woodside": 15245,
}

# % flats (purpose-built + converted) from Census 2021 TS044
census_pct_flats = {
    "Alexandra Park": 42.5,
    "Bounds Green": 61.2,
    "Bruce Castle": 63.5,
    "Crouch End": 70.6,
    "Fortis Green": 45.0,
    "Harringay": 63.7,
    "Hermitage & Gardens": 56.3,
    "Highgate": 62.2,
    "Hornsey": 66.5,
    "Muswell Hill": 58.8,
    "Noel Park": 51.1,
    "Northumberland Park": 63.9,
    "Seven Sisters": 57.9,
    "South Tottenham": 57.4,
    "St Ann's": 55.1,
    "Stroud Green": 74.5,
    "Tottenham Central": 54.6,
    "Tottenham Hale": 58.0,
    "West Green": 54.1,
    "White Hart Lane": 25.8,
    "Woodside": 66.1,
}

# Total households per ward (for density proxy — households per ward)
census_households = {
    "Alexandra Park": 3318,
    "Bounds Green": 4095,
    "Bruce Castle": 5104,
    "Crouch End": 6086,
    "Fortis Green": 4878,
    "Harringay": 6185,
    "Hermitage & Gardens": 3069,
    "Highgate": 5775,
    "Hornsey": 6705,
    "Muswell Hill": 3812,
    "Noel Park": 5342,
    "Northumberland Park": 5647,
    "Seven Sisters": 3456,
    "South Tottenham": 5444,
    "St Ann's": 4073,
    "Stroud Green": 4921,
    "Tottenham Central": 6038,
    "Tottenham Hale": 4036,
    "West Green": 5849,
    "White Hart Lane": 5068,
    "Woodside": 6187,
}

# Calculate ward areas from GeoJSON (approximate using lat/lon -> metres)
def polygon_area_hectares(poly):
    """Approximate area in hectares from lat/lon polygon."""
    coords = list(poly.exterior.coords)
    # Use the shoelace formula with approximate metre conversion
    lat_mid = sum(c[1] for c in coords) / len(coords)
    m_per_deg_lat = 111320.0
    m_per_deg_lon = 111320.0 * math.cos(math.radians(lat_mid))

    n = len(coords)
    area_sq_m = 0.0
    for i in range(n):
        j = (i + 1) % n
        x1 = coords[i][0] * m_per_deg_lon
        y1 = coords[i][1] * m_per_deg_lat
        x2 = coords[j][0] * m_per_deg_lon
        y2 = coords[j][1] * m_per_deg_lat
        area_sq_m += x1 * y2 - x2 * y1

    return abs(area_sq_m) / 2.0 / 10000.0  # convert sq m to hectares

ward_areas = {}
for name, shp in ward_shapes.items():
    ward_areas[name] = polygon_area_hectares(shp)

# Population density (persons per hectare)
pop_density = {}
for w in census_population:
    if ward_areas.get(w, 0) > 0:
        pop_density[w] = census_population[w] / ward_areas[w]

print("\nPopulation density (persons/hectare):")
for w in sorted(pop_density.keys()):
    print(f"  {w}: {pop_density[w]:.1f} p/ha (area: {ward_areas[w]:.1f} ha)")

# ============================================================
# 4. FIXMYSTREET REPORTS (from research agent scrape)
# ============================================================
fixmystreet_counts = {
    "Alexandra Park": 40,
    "Bounds Green": 282,
    "Bruce Castle": 52,
    "Crouch End": 25,
    "Fortis Green": 119,
    "Harringay": 132,
    "Hermitage & Gardens": 127,
    "Highgate": 185,
    "Hornsey": 51,
    "Muswell Hill": 79,
    "Noel Park": 255,
    "Northumberland Park": 55,
    "Seven Sisters": 79,
    "South Tottenham": 85,
    "St Ann's": 63,
    "Stroud Green": 52,
    "Tottenham Central": 142,
    "Tottenham Hale": 58,
    "West Green": 125,
    "White Hart Lane": 59,
    "Woodside": 183,
}

# Normalise per capita (reports per 1000 residents)
fixmystreet_per_1k = {}
for w in fixmystreet_counts:
    fixmystreet_per_1k[w] = (fixmystreet_counts[w] / census_population[w]) * 1000

print("\nFixMyStreet reports per 1000 residents:")
for w in sorted(fixmystreet_per_1k, key=lambda x: fixmystreet_per_1k[x], reverse=True):
    print(f"  {w}: {fixmystreet_per_1k[w]:.1f} ({fixmystreet_counts[w]} reports)")

# ============================================================
# 5. TfL STATION USAGE (annual entries+exits 2023)
# ============================================================
# Station -> ward mapping with combined TfL + NR usage
station_usage = {
    "Alexandra Park": 1_595_988,      # NR only
    "Bounds Green": 4_266_560,        # LU
    "Bruce Castle": 2_574_117 + 1_387_826,  # Bruce Grove LO + NR
    "Crouch End": 0,                  # no station
    "Fortis Green": 0,               # no station
    "Harringay": 1_875_274 + 1_034_164,  # Harringay GL LO + Harringay NR
    "Hermitage & Gardens": 0,        # no station
    "Highgate": 4_408_040,           # LU
    "Hornsey": 1_500_360,            # NR only
    "Muswell Hill": 0,               # no station
    "Noel Park": 7_948_900,          # Turnpike Lane LU
    "Northumberland Park": 943_776,  # NR only
    "Seven Sisters": 12_165_434 + 7_562_722,  # LU + NR
    "South Tottenham": 1_668_645 + 1_260_200 + 1_084_954 + 695_744,  # South Tot LO+NR + Stamford Hill LO+NR
    "St Ann's": 0,                   # no station
    "Stroud Green": 1_149_023 + 857_934,  # Crouch Hill LO + NR (Finsbury Park is on border, not counted)
    "Tottenham Central": 0,          # no station (nearest is Bruce Grove)
    "Tottenham Hale": 13_239_937 + 8_498_156,  # LU + NR
    "West Green": 0,                 # no station
    "White Hart Lane": 1_897_338 + 2_593_686,  # LO + NR
    "Woodside": 9_088_053,           # Wood Green LU
}

print("\nStation usage (annual entries+exits):")
for w in sorted(station_usage, key=lambda x: station_usage[x], reverse=True):
    if station_usage[w] > 0:
        print(f"  {w}: {station_usage[w]:,}")

# ============================================================
# 6. IMD 2019 — LSOA-level, aggregate to wards via point-in-polygon
# ============================================================
print("\nProcessing IMD 2019 data...")

# Read LSOA-level IMD data for Haringey (LA code E09000014)
imd_lsoa = {}  # lsoa_code -> {score, population, lat, lon}

with open('imd2019_file7.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Local Authority District code (2019)') == 'E09000014':
            lsoa = row['LSOA code (2011)']
            try:
                score = float(row['Living Environment Score'])
                pop = int(row['Total population: mid 2015 (excluding prisoners)'])
                imd_lsoa[lsoa] = {'score': score, 'population': pop}
            except (ValueError, KeyError):
                pass

print(f"  Found {len(imd_lsoa)} Haringey LSOAs")

# We need LSOA centroids to map them to wards. Let's use the IMD index of multiple deprivation
# rank to approximate — but we actually need coordinates.
# Let's fetch LSOA Population Weighted Centroids from ONS
# For now, use a simpler approach: read LSOA names to guess ward mapping

# Alternative approach: use the full IMD file which has LSOA names
imd_by_ward = defaultdict(lambda: {'total_score': 0, 'total_pop': 0})

# Re-read to get LSOA names
with open('imd2019_file7.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Local Authority District code (2019)') == 'E09000014':
            lsoa_name = row.get('LSOA name (2011)', '')
            try:
                score = float(row['Living Environment Score'])
                pop = int(row['Total population: mid 2015 (excluding prisoners)'])
                imd_rank = int(row['Living Environment Rank (where 1 is most deprived)'])
                imd_decile = int(row['Living Environment Decile (where 1 is most deprived 10% of LSOAs)'])
            except (ValueError, KeyError):
                continue

            # LSOA names are like "Haringey 001A", "Haringey 001B" etc
            # We can't directly map these to 2022 wards without a lookup
            # Store for later processing
            imd_lsoa[row['LSOA code (2011)']] = {
                'name': lsoa_name,
                'score': score,
                'population': pop,
                'rank': imd_rank,
                'decile': imd_decile
            }

# IMD: We have LSOA-level data but no LSOA-to-2022-ward lookup readily available.
# Instead of fabricating a mapping, we'll use pct_flats and pop_density as structural
# deprivation proxies (both from Census 2021, both at ward level, both real).
# The IMD pattern closely tracks these variables anyway.
print("  Skipping ward-profiles.csv (encoding issues, not needed)")

# ============================================================
# 7. VOA COMMERCIAL PREMISES — LSOA level
# ============================================================
print("\nProcessing VOA data...")
voa_by_lsoa = {}

with open('voa_stock_2023/table_SOP_OA1_1.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = None
    for row in reader:
        if not headers:
            headers = row
            continue
        if len(row) < 3:
            continue
        la_code = row[1] if len(row) > 1 else ''
        if 'E09000014' in str(la_code) or 'Haringey' in str(row):
            lsoa_code = row[0]
            if lsoa_code.startswith('E01'):
                try:
                    total = int(row[2]) if len(row) > 2 else 0
                    voa_by_lsoa[lsoa_code] = total
                except ValueError:
                    pass

print(f"  Found {len(voa_by_lsoa)} Haringey LSOAs in VOA data")
if voa_by_lsoa:
    total_premises = sum(voa_by_lsoa.values())
    print(f"  Total commercial premises: {total_premises}")

# ============================================================
# SINCE WE CAN'T EASILY MAP LSOAs TO 2022 WARDS WITHOUT A LOOKUP,
# LET'S USE THE DATA WE HAVE AT WARD LEVEL AND NOTE THE LIMITATION
# ============================================================

# For IMD and VOA, we'll use proxy indicators:
# - Food outlet density (FSA) as proxy for commercial activity
# - Population density as structural indicator
# - % flats captures housing deprivation element

# ============================================================
# 8. NORMALISE ALL INDICATORS (min-max to 0-10)
# ============================================================
print("\n" + "="*60)
print("FINAL INDICATOR SET (all real data)")
print("="*60)

wards = sorted(ward_shapes.keys())

def min_max_normalise(values_dict):
    """Normalise dictionary values to 0-10 scale."""
    vals = list(values_dict.values())
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return {k: 5.0 for k in values_dict}
    return {k: round(((v - mn) / (mx - mn)) * 10, 1) for k, v in values_dict.items()}

# Calculate food outlets per 1000 residents
food_per_1k = {}
for w in wards:
    pop = census_population.get(w, 1)
    outlets = food_outlet_counts.get(w, 0)
    food_per_1k[w] = (outlets / pop) * 1000

# Indicators to normalise
raw_indicators = {
    'fixmystreet': fixmystreet_per_1k,
    'food_outlets': food_per_1k,
    'pct_flats': census_pct_flats,
    'pop_density': pop_density,
    'station_usage': station_usage,
}

normalised = {}
for key, raw in raw_indicators.items():
    normalised[key] = min_max_normalise(raw)
    print(f"\n{key} (normalised 0-10):")
    for w in sorted(wards, key=lambda x: normalised[key].get(x, 0), reverse=True):
        print(f"  {w}: {normalised[key][w]:.1f} (raw: {raw[w]:.1f})" if isinstance(raw[w], float) else f"  {w}: {normalised[key][w]:.1f} (raw: {raw[w]:,})")

# ============================================================
# 9. COMPOSITE RSI SCORE
# ============================================================
# Revised weights for 5 indicators (must sum to 1.0)
weights = {
    'fixmystreet': 0.30,    # Direct demand signal - reports
    'food_outlets': 0.20,   # Litter source - food outlet density
    'pct_flats': 0.15,      # Housing type - flats/HMOs
    'pop_density': 0.20,    # Population pressure
    'station_usage': 0.15,  # Footfall / transit demand
}

print(f"\nWeights sum: {sum(weights.values())}")

rsi_scores = {}
for w in wards:
    rsi = 0
    for ind, weight in weights.items():
        rsi += normalised[ind].get(w, 0) * weight
    rsi_scores[w] = round(rsi, 1)

print("\n" + "="*60)
print("COMPOSITE RSI SCORES")
print("="*60)
for w in sorted(wards, key=lambda x: rsi_scores[x], reverse=True):
    print(f"  {w}: {rsi_scores[w]:.1f}")

# ============================================================
# 10. OUTPUT AS JAVASCRIPT FOR index.html
# ============================================================

# KBT surveyor notes (from the real 2017/18 reports)
kbt_notes = {
    "Alexandra Park": "Among the best wards surveyed. Detritus was the main issue, with leaf fall contributing to problems on residential roads.",
    "Crouch End": "Leaf fall heavy. Retail areas acceptable for litter but residential roads off retail areas heavily affected.",
    "Fortis Green": "Litter better than other areas surveyed. Graffiti observed on utility boxes and alleyway walls.",
    "Harringay": "Serious detritus on Ladder streets. Fly-tipping observed near Haringey Passage.",
    "Highgate": "Detritus was the main issue. Leaf fall not cleared, causing related drainage and slip problems.",
    "Noel Park": "Heavy litter on side streets off the high street. KBT noted 'considerably different frequencies of cleansing' as the cause of variation between main retail area and surrounding streets.",
    "Northumberland Park": "Among the least favourable of all wards for every element surveyed. Massive fly-tips observed. Leeside Road had 'one of the most significant fly-tips the surveyor had ever seen.' Industrial areas severely affected.",
    "Bruce Castle": "Litter and graffiti prevalent on footpaths. Vandalised utility boxes observed throughout the ward.",
    "Tottenham Hale": "Residential areas near the High Road had serious litter issues. Fly-tipping around Roseberry Avenue and Carbuncle Passage.",
    "Woodside": "Among the best for litter and detritus. Graffiti was a serious issue in industrial areas.",
}

indicator_labels = {
    'fixmystreet': 'FixMyStreet reports',
    'food_outlets': 'Food outlet density',
    'pct_flats': '% flats (Census 2021)',
    'pop_density': 'Population density',
    'station_usage': 'Station usage (TfL/NR)',
}

# Build the JS object
lines = ['const wardData = {']
for w in wards:
    kbt = kbt_notes.get(w)
    kbt_str = f'"{kbt}"' if kbt else 'null'

    lines.append(f'  "{w}": {{')
    lines.append(f'    rsi: {rsi_scores[w]},')
    lines.append(f'    indicators: {{')
    for ind_key in weights:
        label = indicator_labels[ind_key]
        score = normalised[ind_key].get(w, 0)
        # Also include raw value
        if ind_key == 'fixmystreet':
            raw = f"{fixmystreet_per_1k[w]:.1f} per 1k residents ({fixmystreet_counts[w]} total)"
        elif ind_key == 'food_outlets':
            raw = f"{food_per_1k[w]:.1f} per 1k residents ({food_outlet_counts.get(w, 0)} outlets)"
        elif ind_key == 'pct_flats':
            raw = f"{census_pct_flats[w]:.1f}%"
        elif ind_key == 'pop_density':
            raw = f"{pop_density[w]:.0f} persons/ha"
        elif ind_key == 'station_usage':
            raw = f"{station_usage[w]:,} annual entries+exits" if station_usage[w] > 0 else "No station in ward"

        lines.append(f'      {ind_key}: {{ score: {score}, label: "{label}", raw: "{raw}" }},')
    lines.append(f'    }},')
    lines.append(f'    kbt: {kbt_str}')
    lines.append(f'  }},')

lines.append('};')

js_output = '\n'.join(lines)

with open('ward_data_real.js', 'w') as f:
    f.write(js_output)

print("\n\nJavaScript output written to ward_data_real.js")

# Also output the weights
weights_js = "const weights = {\n"
for k, v in weights.items():
    weights_js += f"  {k}: {v},\n"
weights_js += "};"
print(f"\n{weights_js}")

# Summary stats
print(f"\nSummary:")
print(f"  Wards: {len(wards)}")
print(f"  Indicators: {len(weights)}")
print(f"  RSI range: {min(rsi_scores.values())} - {max(rsi_scores.values())}")
print(f"  Mean RSI: {sum(rsi_scores.values())/len(rsi_scores):.1f}")
