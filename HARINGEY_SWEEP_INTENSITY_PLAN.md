# Haringey Required Sweep Intensity Index (RSI)

## Project summary

A publicly available, ward-level composite index that estimates the **required street cleansing intensity** for each area of Haringey, based entirely on open data. The index is designed to demonstrate that a uniform once-per-week residential sweep schedule is allocatively inefficient — over-serving low-demand areas in the west while under-serving high-demand areas in the east.

The output is an interactive map of Haringey at ward level (21 wards post-2022 boundary changes), with each ward scored and colour-coded by required sweep intensity. Users can click a ward to see the component scores that drive the overall rating. The methodology is fully transparent and documented alongside the map.

---

## Prior art: what already exists

### Philadelphia Litter Index (direct model)
Philadelphia's Zero Waste and Litter Cabinet developed a city-wide Litter Index from 2017. It uses a 1–4 rating system (derived from Keep America Beautiful's Community Appearance Index) applied at block level by trained surveyors across six city departments. The data is published on CleanPHL.org and Open Data Philly, where residents can look up their block's score. The city uses it for camera placement, street sweeping pilot selection, bin placement, and neighbourhood litter control plans. The key finding relevant to us: areas with high litter scores and low 311 (reporting) volumes were identified as underserved — exactly the dynamic we suspect in east Haringey. Philadelphia also found that being near arterial streets, food-serving businesses, and vacant properties correlated with higher litter, while park proximity correlated with lower litter.

### Keep Britain Tidy NI195 / LEQ methodology
The established UK methodology for measuring local environmental quality. Uses trained surveyors grading sites A–D for litter, detritus, graffiti, and fly-posting. Previously a national indicator (NI195), now a paid service from KBT.

**Crucially, we have Haringey-specific KBT reports.** In 2017/18 Haringey commissioned KBT to carry out independent LEQ surveys across 10 wards in two tranches (320 sites per tranche, 64 per ward, graded A through D on a 7-point scale). The findings are devastating for the uniform-provision argument:

- **Haringey was 2–3x worse than the London benchmark on every measure.** Litter: 10–13% of sites failing vs a London average of ~4%. Detritus: 7–15% vs ~4.5%. Graffiti: 7–10% vs ~2.5%.
- **The east-west ward split is stark.** Northumberland Park "generally fared among the least favourable of all wards for each element" with massive fly-tips (Leeside Road: "one of the most significant fly-tips the surveyor had ever seen"). Alexandra ward and Fortis Green "generally fared among the best." Bruce Grove and Tottenham Hale both had serious litter and fly-tipping problems.
- **KBT surveyors directly identified the cleansing frequency gap.** In Noel Park, they noted "a noticeable difference between Litter standards seen in the Main Retail area and the surrounding streets, caused by considerably different frequencies of cleansing." In Tottenham Hale, residential areas near the High Road had serious litter issues attributed to proximity to shops and higher footfall.
- **Industry/warehousing and Other Highways were catastrophic** — 22–45% of sites below acceptable standard for litter, far worse than housing areas. These land uses are concentrated in the east.
- **The "broken windows" dynamic was observed.** Graffiti was visible on over a third of all transects. KBT noted this creates a sense of an area being "uncared for" which "can exacerbate other LEQ issues, as well as potentially leading to other, more serious crimes."

These reports are from 2017/18 and use the old ward boundaries. But they provide independent professional observational evidence — the gold standard for LEQ assessment — confirming the pattern our proxy indicators will show. They should be cited prominently in the RSI narrative. FOI for any subsequent KBT reports (the council may have continued commissioning them) would be valuable.

### APSE Performance Networks
The Association for Public Service Excellence benchmarks street cleansing across 300+ UK councils. Includes cost per household, satisfaction surveys, and percentage of sites below Grade B. Useful for borough-level comparison but not sub-borough analysis.

### DEFRA WasteDataFlow
National fly-tipping database. Published annually at local authority level. Gives Haringey's total incidents, breakdown by waste type and land type, enforcement actions, and costs. Does not give sub-borough geography.

**Bottom line: nothing exists at ward level for Haringey that combines demand indicators into a composite score. We're building something new, but the Philadelphia model gives us a strong methodological spine. And unlike Philadelphia when they started, we already have independent professional observational data (the KBT reports) confirming the pattern our demand model will surface. That's a powerful one-two: "here's what the demand data predicts, and here's what trained surveyors actually found on the ground."**

---

## The RSI measure: design principles

1. **Use only publicly available data.** Every input must be obtainable without FOI, council cooperation, or payment. This makes the index independently reproducible and politically harder to dismiss.

2. **Preference for operational/observed data over structural proxies.** FixMyStreet reports, fly-tipping incidents, and food outlet counts are more persuasive than deprivation indices because they measure actual litter-generating activity rather than inferred risk. But structural factors (deprivation, housing type, population density) still matter as contextual multipliers.

3. **Transparency over sophistication.** Every component score and its weight is visible. A councillor should be able to understand why their ward scores what it does. No black boxes.

4. **The index measures *required intensity*, not current performance.** We're not grading how clean streets are today — we're estimating how much cleaning each area *needs* based on observable demand signals and environmental risk factors. However, the 2017/18 KBT LEQ reports give us a historical baseline of actual observed cleanliness by ward, and these can be referenced as corroborating evidence alongside the RSI. If the RSI's demand-based score and KBT's outcome-based observations both point in the same direction — which they will — the case becomes extremely difficult to dismiss.

5. **Anchor the methodology in established practice.** The KBT NI195/LEQ methodology is the UK's accepted standard for local environmental quality assessment. Our RSI doesn't replace it — it complements it by modelling *demand* where KBT measures *outcome*. Framing the RSI as sitting alongside, not competing with, KBT methodology gives it credibility with council officers who know the NI195 system.

---

## Component indicators

The RSI is built from two tiers of indicators:

### Tier 1: Direct demand signals (weight: 70%)

These are observed measures of actual litter/waste problems.

| # | Indicator | Source | Geography | How to obtain |
|---|-----------|--------|-----------|---------------|
| 1a | **FixMyStreet reports** — volume of street cleaning, litter, fly-tipping, and rubbish reports per ward | FixMyStreet.com | Point data, geocoded to ward | Scrape from fixmystreet.com/reports/Haringey — publicly browsable by ward. Count reports in relevant categories over trailing 12 months. Note: biased toward digitally engaged populations, but this *strengthens* the argument — if east Haringey still scores high despite likely under-reporting, the true picture is worse. |
| 1b | **Love Clean Streets / council CRM reports** | Haringey Council (may need FOI) | Ward level if available | The council's own app (Love Clean Streets / "Our Haringey") captures reports. If not published, FOI the volume of street cleansing and fly-tipping reports by ward for the last 12 months. Fallback: omit and note the gap. |
| 1c | **Fly-tipping heat map** | Haringey Fly-Tipping Strategy 2019 (public, on council minutes) | Sub-borough (mapped) | The 2019 strategy includes a heat map showing Tottenham High Road corridor as the highest concentration. Digitise this as a ward-level relative score. Request updated version via FOI if needed. |
| 1d | **Food Standards Agency registered premises** | food.gov.uk/ratings | Postcode, geocodable to ward | Download all FSA-registered food businesses in Haringey. Filter for takeaway/fast food categories. Count per ward. Takeaway density is a strong litter-generation proxy — the council's own public health data acknowledges Tottenham has an "overconcentration of fast food outlets." |
| 1e | **Commercial waste premises** | Haringey commercial waste licensing (FOI if not published) | Address level | Number of businesses with commercial waste contracts or duty of care notices. More commercial activity = more litter generation. Fallback: use VOA business rates data (publicly searchable) as proxy for commercial density. |

### Tier 2: Structural/contextual risk factors (weight: 30%)

These don't directly measure litter but indicate conditions that research shows correlate with higher litter demand.

| # | Indicator | Source | Geography | How to obtain |
|---|-----------|--------|-----------|---------------|
| 2a | **IMD 2025 — Living Environment domain** | MHCLG via data.gov.uk | LSOA, aggregable to ward | Download IMD 2025 LSOA-level data. Use the Living Environment deprivation domain (or overall IMD rank). Average LSOA scores within each ward. The 2025 IMD was recently published. Keep Britain Tidy research shows the most deprived areas have 3x more litter. |
| 2b | **Housing type — % flats/HMOs** | Census 2021 via NOMIS | Ward / LSOA | Flats and HMOs have communal waste areas, less individual ownership of the street, and higher fly-tipping risk (especially at tenancy changeover). Extract % of households in flats or shared dwellings per ward. |
| 2c | **Population density** | Census 2021 via NOMIS or GLA population estimates | Ward | More people per hectare = more litter generation. Simple residents per hectare. |
| 2d | **Footfall proxy — TfL bus/tube passenger numbers** | TfL open data | Station/stop level, allocable to ward | High-footfall areas (stations, bus interchanges, high streets) generate disproportionate litter. TfL publishes annual entries/exits for tube stations and bus route usage. Allocate station footfall to wards. |
| 2e | **Retail/high street frontage** | OS AddressBase or VOA ratings list | Address level, aggregable to ward | Length of commercial/retail high street frontage per ward. More high street = more litter from packaging, smoking, food-on-the-go. VOA ratings list is publicly searchable; OS data requires a license but OpenStreetMap can approximate. |

---

## Scoring methodology

### Step 1: Normalise each indicator
For each indicator, calculate the ward-level value, then normalise to a 0–10 scale using min-max normalisation across Haringey's 21 wards:

```
ward_score = ((ward_value - min_value) / (max_value - min_value)) * 10
```

This means the ward with the highest value on any indicator scores 10, the lowest scores 0, and others are distributed proportionally.

### Step 2: Weight and combine
Apply the following weights (adjustable, transparent):

**Tier 1 — Direct demand (70% total):**
- 1a. FixMyStreet reports: 20%
- 1b. Council CRM reports: 15% (or redistribute to 1a if unavailable)
- 1c. Fly-tipping concentration: 15%
- 1d. Takeaway/food outlet density: 10%
- 1e. Commercial premises density: 10%

**Tier 2 — Structural context (30% total):**
- 2a. IMD Living Environment score: 10%
- 2b. Housing type (% flats/HMOs): 5%
- 2c. Population density: 5%
- 2d. Footfall (TfL data): 5%
- 2e. Retail frontage: 5%

### Step 3: Calculate composite RSI

```
RSI = Σ (indicator_normalised_score × indicator_weight)
```

Result: each ward gets an RSI score from 0 to 10.

### Step 4: Band the scores

| RSI band | Label | Implied sweep frequency |
|----------|-------|------------------------|
| 0–2 | Low | Fortnightly may suffice |
| 2–4 | Standard | Weekly (current baseline) |
| 4–6 | Elevated | 2x per week |
| 6–8 | High | 3x per week or daily on key streets |
| 8–10 | Critical | Daily sweep + targeted enforcement |

The "implied sweep frequency" column is illustrative — it's what we argue the data suggests, not what the council currently provides.

---

## Claude Code build spec

This section is the complete brief for building the output in Claude Code. The output is a **single-page interactive HTML application** with two sections: (1) an interactive choropleth map of the RSI, and (2) a scrolling narrative that makes the political and evidential argument for variable-frequency sweeping.

### Ward data

**Ward boundaries:** Haringey has 21 wards (post-May 2022 boundary changes). Boundaries are available from MapIt (mapit.mysociety.org). The 21 ward IDs in MapIt are:

```
165543: Alexandra Park
165538: Bounds Green
165655: Bruce Castle
165539: Crouch End
165537: Fortis Green
165488: Harringay
165547: Hermitage & Gardens
165487: Highgate
165542: Hornsey
165541: Muswell Hill
165544: Noel Park
165553: Northumberland Park
165548: Seven Sisters
165654: South Tottenham
165546: St Ann's
165540: Stroud Green
165552: Tottenham Central
165550: Tottenham Hale
165549: West Green
165551: White Hart Lane
165545: Woodside
```

To get GeoJSON for each ward: `https://mapit.mysociety.org/area/{id}.geojson`
To get all wards at once: `https://mapit.mysociety.org/areas/{comma-separated-ids}.geojson`

If MapIt is rate-limited or slow, hardcode a simplified GeoJSON. Ward centroids can be approximated from the boundary polygons.

### RSI scores: use realistic illustrative data

We don't yet have the scraped/collected real data for every indicator. For this build, **create a plausible illustrative dataset** based on what we know from the KBT reports, the fly-tipping strategy, the IMD data, and local knowledge. The scores should reflect reality closely enough to demonstrate the tool — the exact numbers will be replaced with real data later.

Use these principles to construct the illustrative data:

**High RSI (7–10) — eastern wards with high deprivation, high commercial activity, high density:**
- Northumberland Park, Tottenham Hale, White Hart Lane, Bruce Castle, Tottenham Central, West Green

**Medium RSI (4–7) — mixed wards, some commercial corridors:**
- Seven Sisters, South Tottenham, Noel Park, St Ann's, Harringay, Woodside, Bounds Green

**Low RSI (1–4) — western wards, low density, affluent:**
- Alexandra Park, Highgate, Muswell Hill, Fortis Green, Crouch End, Hornsey, Stroud Green, Hermitage & Gardens

For each ward, create plausible component scores (0–10 normalised) for:
- FixMyStreet report volume (weight 20%)
- Council complaint volume (weight 15%)
- Fly-tipping concentration (weight 15%)
- Takeaway/food outlet density (weight 10%)
- Commercial premises density (weight 10%)
- IMD deprivation score (weight 10%)
- Housing type — % flats/HMOs (weight 5%)
- Population density (weight 5%)
- Footfall proxy (weight 5%)
- Retail frontage (weight 5%)

Mark the data clearly as illustrative with a banner: "Scores shown are illustrative, based on published data and local knowledge. Full dataset with sourced figures in preparation."

---

### Section 1: Interactive map

**Technology:** Single HTML file. Use Leaflet.js from CDN. No build tools.

**Layout:** Full-width map occupying ~60% of viewport height at top of page. Below it, the narrative section scrolls.

**Map features:**

1. **Choropleth.** Wards filled by RSI score. Colour scale: dark green (0–2) → light green (2–4) → amber (4–6) → orange (6–8) → deep red (8–10). Thin white borders between wards. Light grey basemap (CartoDB Positron or similar).

2. **Hover.** On hover, ward name and RSI score appear in a tooltip. Ward boundary highlights (thicker border or slight opacity change).

3. **Click panel.** Clicking a ward opens a side panel (or overlay on mobile) showing:
   - Ward name, RSI score, RSI band label (e.g. "Critical — daily sweep needed")
   - Horizontal stacked bar showing the contribution of each component to the overall score, colour-coded by tier (blue for Tier 1 direct demand, grey for Tier 2 structural)
   - A row for each indicator showing the raw illustrative value and its normalised score
   - A short text note: what the KBT surveyors found in this ward if it was one of the 10 surveyed wards (pull a 1–2 sentence summary from the reports for: Alexandra Park → "Among the best wards. Detritus was the main issue." / Northumberland Park → "Among the least favourable for every element. Massive fly-tips. Industrial areas severely affected." / Noel Park → "Heavy litter on side streets off high street. KBT noted 'considerably different frequencies of cleansing' as the cause." / Bruce Castle → mapped from Bruce Grove T2 observations: "Litter and graffiti on footpaths. Vandalised utility boxes throughout." / Tottenham Hale → "Residential areas near High Road had serious litter. Fly-tipping around Roseberry Avenue and Carbuncle Passage." / Crouch End → "Leaf fall heavy. Retail areas acceptable for litter but residential roads off retail areas heavily affected." / Fortis Green → "Litter better than other areas. Graffiti on utility boxes and alleyway walls." / Highgate → "Detritus was the main issue. Leaf fall not cleared causing related problems." / Woodside → "Among the best for litter and detritus. Graffiti serious in industrial areas." / Harringay → mapped from Haringey ward T2: "Serious detritus on Ladder streets. Fly-tipping near Haringey Passage.")

4. **Legend.** Fixed position, bottom-left of map. Shows the 5 RSI bands with colours and labels.

5. **Current service overlay.** A toggle or small annotation showing: "Current provision: 1 sweep per week, uniform across all wards" — displayed as a flat horizontal line across a small bar chart next to the legend, making the gap between uniform provision and variable demand visually obvious.

**Design direction:** Data journalism. Light/warm palette. Use a serif font for headings (e.g. Playfair Display or Lora) and a clean sans-serif for body/data (e.g. Source Sans Pro). No council branding. Header: "Haringey Required Sweep Intensity Index" with a subtitle: "Where streets need cleaning most — and where the current schedule falls short". Credit line: "Built with open data. Methodology fully transparent."

---

### Section 2: The narrative argument

Below the map, a scrolling long-form section that makes the case. This is the persuasive core. Structure it as follows. Write the actual prose — don't just outline it. This needs to read like a short piece of investigative data journalism.

#### 2a. The headline finding

Open with the core stat. Something like:

> Haringey gives every residential road one street sweep per week. But the data shows that demand for cleaning varies by a factor of five or more across the borough. Wards in the east — Northumberland Park, Tottenham Hale, White Hart Lane — face dramatically higher litter generation from denser housing, more takeaway outlets, higher footfall, and more fly-tipping. Yet they receive exactly the same service as Muswell Hill and Highgate. This isn't just unfair. It's inefficient.

#### 2b. What the professionals found

Draw directly on the KBT reports. Key points to make:

- In 2017/18 Haringey commissioned Keep Britain Tidy — the UK's leading authority on local environmental quality — to independently survey street cleanliness across the borough.
- Haringey scored 2–3x worse than the London average for litter, detritus, graffiti and fly-posting.
- The east-west split was clear. Northumberland Park was the worst ward. Alexandra was the best.
- KBT surveyors identified the cause directly: in Noel Park they recorded "a noticeable difference between Litter standards seen in the Main Retail area and the surrounding streets, caused by considerably different frequencies of cleansing."
- In Northumberland Park, Leeside Road had "one of the most significant fly-tips the surveyor had ever seen."
- Industry and warehousing areas — concentrated in the east — had 22–45% of sites below acceptable standard.
- The overall cleanliness rating for Haringey on the KBT gauge chart was "Unsatisfactory" for both litter and detritus.

#### 2c. The deprivation overlay

- Haringey is the 6th most deprived borough in London. But deprivation is not evenly distributed.
- In the east of the borough, more than half of small neighbourhoods (LSOAs) fall in the 20% most deprived nationally. In the west, almost none do.
- Keep Britain Tidy's national research shows the most deprived areas have nearly three times as much litter as the least deprived, and litter-free spaces are seven times less likely.
- A uniform service level in the face of this unequal demand is regressive. The areas that need the most get the same as those that need the least.

#### 2d. The fly-tipping crisis

- Haringey has consistently been among the worst London boroughs for fly-tipping. DEFRA data recorded over 34,000 incidents in one year — second only to Enfield.
- The council's own 2019 fly-tipping strategy acknowledged that the Tottenham High Road corridor has the highest concentration, with further hotspots in West Green and Wood Green.
- In 2024/25, the council issued 2,554 fines totalling £1.3 million and deployed 15 additional enforcement officers. The problem persists.

#### 2e. Other boroughs are moving to demand-led models

This is the Greenwich comparator. Key points:

- In 2024, Royal Borough of Greenwich approved a move to **variable frequency sweeping according to speed of degradation of public realm**, using route optimisation software and local knowledge.
- Greenwich divided the borough into 8 managed areas, each with a supervisor accountable for standards. Residential streets would be cleaned by individual sweepers with barrows on regular beats — not by roaming teams.
- The model is explicit: areas that degrade faster get cleaned more often. Areas that stay cleaner get cleaned less. Same budget, smarter allocation.
- Greenwich estimated savings of £150k in year one rising to £1.2 million by 2028 — through efficiency, not cuts.
- Haringey still operates the uniform model that Greenwich has abandoned.

Also note (if space): Philadelphia's Litter Index programme uses block-level scoring to drive variable cleaning schedules, camera placement, and bin siting. The principle — measure demand, allocate accordingly — is now standard practice in well-run cleansing operations internationally.

#### 2f. What the council already knows

- The council moved from twice-weekly to once-weekly sweeping in January 2016 to save £860,000. Performance dropped immediately and was noted in their own scrutiny panel.
- They commissioned the KBT survey which told them standards were failing, particularly in the east.
- Their fly-tipping strategy acknowledged the geographic concentration of the problem.
- Their public health data acknowledges the overconcentration of fast food outlets in Tottenham.
- The Veolia contract runs to 2027. That contract renegotiation is the moment to shift from input-based KPIs (sweeps per road) to outcome-based KPIs (cleanliness to a standard).

#### 2g. The ask

Close with the specific, achievable ask. Not "more money for street cleaning" but:

1. **Publish ward-level cleansing data.** The council holds complaint volumes, sweep schedules, and enforcement data by area. Publish it, so residents can see how their ward is served.
2. **Move to demand-weighted scheduling.** Follow Greenwich: use the data to sweep high-demand areas more often and low-demand areas less often. Same budget, better outcomes.
3. **Commission an updated LEQ survey.** The last independent survey was 2017/18. Seven years without a check on standards is not acceptable. An updated KBT survey would establish whether things have improved or deteriorated.
4. **Build demand-based KPIs into the next Veolia contract.** When the contract comes up in 2027, specify outcomes (cleanliness to Grade B standard across all wards) rather than inputs (one sweep per week everywhere).

---

### Section 3: Methodology transparency

A collapsible/expandable section at the bottom. Include:

- Full list of indicators, sources, weights
- The normalisation formula
- The banding thresholds
- A note on illustrative vs real data
- Links to all source datasets
- An invitation: "If the council has better data, we'd welcome it. Publish your ward-level complaint volumes, sweep schedules, and inspection scores, and we'll incorporate them."

---

### Technical notes for build

- **Single HTML file.** Everything self-contained. Leaflet.js, fonts, and any chart libraries loaded from CDNs.
- **Mobile responsive.** The audience includes councillors reading on phones and residents sharing on WhatsApp. Map should work at 375px width. Side panel becomes bottom sheet on mobile.
- **Print-friendly.** A print stylesheet that renders the map as a static image (or hides it) and keeps the narrative readable.
- **No server.** Fully static. Can be hosted on GitHub Pages, Netlify, or served as a local file.
- **Ward boundary source.** Use MapIt: `https://mapit.mysociety.org/areas/165543,165538,165655,165539,165537,165488,165547,165487,165542,165541,165544,165553,165548,165654,165546,165540,165552,165550,165549,165551,165545.geojson` — or if that's unreliable at build time, pre-fetch and embed the GeoJSON inline in the HTML.
- **Data inline.** Embed the ward scores as a JS object in the HTML. No external JSON fetch needed.
- **Scroll-driven interaction (optional nice-to-have).** As the user scrolls through the narrative sections, the map could highlight the relevant wards (e.g. when reading about Northumberland Park, that ward pulses on the map). This is a nice touch but not essential for v1.

---

## Data collection plan

### Immediately available (no FOI needed)

| Data | Source | Action |
|------|--------|--------|
| FixMyStreet reports | fixmystreet.com/reports/Haringey | Scrape by ward, filter by category, count 12-month totals |
| IMD 2025 LSOA scores | MHCLG / data.gov.uk | Download, filter to Haringey LSOAs, aggregate to ward |
| FSA food business ratings | food.gov.uk/ratings API | Download Haringey, filter to takeaway categories, geocode to ward |
| Census 2021 housing/population | NOMIS (nomisweb.co.uk) | Download ward-level tables for housing type and population density |
| TfL station entries | TfL open data | Download annual station usage, allocate to wards |
| Ward boundaries GeoJSON | MapIt (mapit.mysociety.org) | Fetch for all 21 ward IDs listed above |
| Fly-tipping strategy heat map | Haringey council minutes (public) | Digitise from the 2019 strategy document |
| VOA business rates (commercial density) | VOA rating list search | Search by postcode for Haringey, count commercial properties per ward |
| KBT LEQ survey reports 2017/18 (T1 & T2) | In hand (uploaded) | Ward-level surveyor observations and NI195 scores for 10 wards. Use as corroborating narrative evidence. Map old ward observations to new boundaries where possible. |

### May need FOI

| Data | Source | FOI wording |
|------|--------|-------------|
| Council CRM report volumes by ward | Haringey Council | "Total number of service requests relating to (a) street cleansing, (b) fly-tipping, (c) litter, and (d) overflowing bins received by the council, broken down by ward, for each of the last 3 financial years." |
| Veolia sweep schedule/routes | Haringey Council / Veolia | "The current street sweeping schedule for residential roads, including frequency of sweeping for each road or zone, and any variation in frequency across the borough." |
| Updated fly-tipping heat map | Haringey Council | "A map or dataset showing the geographical distribution of fly-tipping incidents reported to the council in the financial years 2022/23, 2023/24, and 2024/25, at the finest available geography." |
| Enforcement action locations | Haringey Council | "Locations (by ward or postcode) of all fixed penalty notices issued for fly-tipping and littering in 2024/25." |
| Subsequent KBT/LEQ survey reports | Haringey Council | "All Local Environmental Quality survey reports commissioned by the council from Keep Britain Tidy or any other provider since April 2018, including any ward-level or site-level data." |

---

## How the RSI map makes the case

The power of this tool is that it reframes the debate. Instead of "we want more street cleaning" (a spending ask the council can reject), the argument becomes:

1. **Here is the demand** — measured by observable, independently verifiable data
2. **Here is what happened when professionals looked** — the council's own KBT surveys from 2017/18 found Northumberland Park among the worst wards, Alexandra among the best, and Haringey 2–3x worse than the London average on every measure. KBT surveyors explicitly identified variable cleansing frequency as the cause of the gap between main retail areas and surrounding streets.
3. **Here is the current provision** — uniform weekly sweeps, unchanged since the 2016 cut from twice-weekly
4. **Here is the gap** — wards scoring 8+ on RSI are getting the same service as wards scoring 2
5. **Here is what other boroughs are doing** — Greenwich has moved to demand-led variable scheduling. Philadelphia uses block-level data to drive cleaning deployment. Haringey is behind the curve.
6. **The ask is reallocation, not more money** — reduce frequency in low-RSI wards, increase in high-RSI wards

This is an efficiency argument, not a budget argument. It's also an equity argument: the correlation between high RSI scores and high deprivation will be visible on the map. Uniform provision in the face of unequal demand is regressive.

The KBT evidence is particularly powerful because it's the council's own commissioned data. They paid for independent surveyors who told them that standards in the east were failing — and the response was to maintain a uniform schedule. That's the political nub of it.

---

## Risks and limitations

| Risk | Mitigation |
|------|------------|
| **Reporting bias**: FixMyStreet data reflects who reports, not what exists. Digitally engaged, affluent areas may over-report relative to actual conditions. | This actually *helps* the argument. If east Haringey scores high despite likely under-reporting, the true need is even greater. Note this explicitly in methodology. |
| **Data staleness**: Some inputs (Census 2021, IMD 2025 based on ~2022 data) are not current. | Use the most recent available for each indicator. Note dates. The structural picture hasn't changed materially. |
| **Arbitrary weights**: Any composite index involves judgment about what matters more. | Make weights adjustable and transparent. Show sensitivity analysis. If the east-west pattern holds across reasonable weight variations, the finding is robust. |
| **Council pushback**: "Your measure doesn't account for X" | Invite the council to publish their own data. If they have better sub-borough information about demand, great — publish it. The RSI fills a gap they haven't filled. |
| **Ward boundaries are coarse**: 21 wards average ~13,000 people each. Significant variation within wards. | Acknowledge. Note that LSOA-level analysis is possible for IMD and Census data. FixMyStreet data could be mapped at finer geography. Ward level is a starting point. |

---

## Extensions (future phases)

- **FOI the Tranche 3 and any subsequent KBT reports**: We have T1 and T2 of the 2017/18 survey. T3 (December 2017–March 2018) would complete the annual picture. Any subsequent years would show whether things improved. This is low-hanging fruit.
- **Replace illustrative data with real data**: Scrape FixMyStreet, download IMD/Census/FSA, build the real scores.
- **Time-series tracking**: Repeat the RSI data collection quarterly to show trends
- **LSOA-level version**: Finer geography using Census and IMD data, with FixMyStreet points mapped continuously
- **Community litter survey**: Adopt the Philadelphia/KBT model — recruit volunteer surveyors to rate streets on the KBT A–D scale using their published grading definitions (which are in our uploaded reports). This creates *primary* observational data that doesn't depend on reporting behaviour.
- **Comparison tool**: Show Haringey against comparable boroughs (Hackney, Lewisham, Waltham Forest, Enfield) using DEFRA data
- **Integration with council contract KPIs**: If Veolia's contract is renegotiated before 2027, the RSI could inform outcome-based KPIs (pay for cleanliness to a standard, not sweeps per road)
- **Validate RSI against KBT observations**: Check whether the RSI scores for the 10 wards KBT surveyed correlate with their observed NI195 scores. If they do, the model is validated against professional observation.
