const wardData = {
  "Alexandra Park": {
    rsi: 0.9,
    indicators: {
      fixmystreet: { score: 1.0, label: "FixMyStreet reports", raw: "4.5 per 1k residents (40 total)" },
      food_outlets: { score: 1.6, label: "Food outlet density", raw: "4.3 per 1k residents (38 outlets)" },
      imd: { score: 0.0, label: "IMD deprivation score", raw: "12.1 (pop-weighted avg)" },
      pct_flats: { score: 3.4, label: "% flats (Census 2021)", raw: "42.5%" },
      pop_density: { score: 0.0, label: "Population density", raw: "37 persons/ha" },
      station_usage: { score: 0.7, label: "Station usage (TfL/NR)", raw: "1,595,988 annual entries+exits" },
    },
    kbt: "Among the best wards surveyed. Detritus was the main issue, with leaf fall contributing to problems on residential roads."
  },
  "Bounds Green": {
    rsi: 4.8,
    indicators: {
      fixmystreet: { score: 10.0, label: "FixMyStreet reports", raw: "28.7 per 1k residents (282 total)" },
      food_outlets: { score: 2.7, label: "Food outlet density", raw: "5.8 per 1k residents (57 outlets)" },
      imd: { score: 3.0, label: "IMD deprivation score", raw: "22.4 (pop-weighted avg)" },
      pct_flats: { score: 7.3, label: "% flats (Census 2021)", raw: "61.2%" },
      pop_density: { score: 4.2, label: "Population density", raw: "89 persons/ha" },
      station_usage: { score: 2.0, label: "Station usage (TfL/NR)", raw: "4,266,560 annual entries+exits" },
    },
    kbt: null
  },
  "Bruce Castle": {
    rsi: 4.7,
    indicators: {
      fixmystreet: { score: 0.7, label: "FixMyStreet reports", raw: "3.9 per 1k residents (52 total)" },
      food_outlets: { score: 5.5, label: "Food outlet density", raw: "9.4 per 1k residents (127 outlets)" },
      imd: { score: 7.9, label: "IMD deprivation score", raw: "38.9 (pop-weighted avg)" },
      pct_flats: { score: 7.7, label: "% flats (Census 2021)", raw: "63.5%" },
      pop_density: { score: 4.7, label: "Population density", raw: "95 persons/ha" },
      station_usage: { score: 1.8, label: "Station usage (TfL/NR)", raw: "3,961,943 annual entries+exits" },
    },
    kbt: "Litter and graffiti prevalent on footpaths. Vandalised utility boxes observed throughout the ward."
  },
  "Crouch End": {
    rsi: 2.5,
    indicators: {
      fixmystreet: { score: 0.0, label: "FixMyStreet reports", raw: "1.9 per 1k residents (25 total)" },
      food_outlets: { score: 5.3, label: "Food outlet density", raw: "9.1 per 1k residents (119 outlets)" },
      imd: { score: 0.9, label: "IMD deprivation score", raw: "15.2 (pop-weighted avg)" },
      pct_flats: { score: 9.2, label: "% flats (Census 2021)", raw: "70.6%" },
      pop_density: { score: 3.7, label: "Population density", raw: "82 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: "Leaf fall heavy. Retail areas acceptable for litter but residential roads off retail areas heavily affected."
  },
  "Fortis Green": {
    rsi: 1.4,
    indicators: {
      fixmystreet: { score: 2.8, label: "FixMyStreet reports", raw: "9.4 per 1k residents (119 total)" },
      food_outlets: { score: 0.0, label: "Food outlet density", raw: "2.2 per 1k residents (28 outlets)" },
      imd: { score: 0.3, label: "IMD deprivation score", raw: "13.1 (pop-weighted avg)" },
      pct_flats: { score: 3.9, label: "% flats (Census 2021)", raw: "45.0%" },
      pop_density: { score: 2.3, label: "Population density", raw: "65 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: "Litter better than other areas surveyed. Graffiti observed on utility boxes and alleyway walls."
  },
  "Harringay": {
    rsi: 4.0,
    indicators: {
      fixmystreet: { score: 2.7, label: "FixMyStreet reports", raw: "9.1 per 1k residents (132 total)" },
      food_outlets: { score: 5.5, label: "Food outlet density", raw: "9.4 per 1k residents (137 outlets)" },
      imd: { score: 4.0, label: "IMD deprivation score", raw: "25.5 (pop-weighted avg)" },
      pct_flats: { score: 7.8, label: "% flats (Census 2021)", raw: "63.7%" },
      pop_density: { score: 4.4, label: "Population density", raw: "92 persons/ha" },
      station_usage: { score: 1.3, label: "Station usage (TfL/NR)", raw: "2,909,438 annual entries+exits" },
    },
    kbt: "Serious detritus on Ladder streets. Fly-tipping observed near Haringey Passage."
  },
  "Hermitage & Gardens": {
    rsi: 4.2,
    indicators: {
      fixmystreet: { score: 4.9, label: "FixMyStreet reports", raw: "15.1 per 1k residents (127 total)" },
      food_outlets: { score: 6.3, label: "Food outlet density", raw: "10.4 per 1k residents (88 outlets)" },
      imd: { score: 3.4, label: "IMD deprivation score", raw: "23.7 (pop-weighted avg)" },
      pct_flats: { score: 6.3, label: "% flats (Census 2021)", raw: "56.3%" },
      pop_density: { score: 5.0, label: "Population density", raw: "98 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: null
  },
  "Highgate": {
    rsi: 2.6,
    indicators: {
      fixmystreet: { score: 4.7, label: "FixMyStreet reports", raw: "14.5 per 1k residents (185 total)" },
      food_outlets: { score: 2.4, label: "Food outlet density", raw: "5.4 per 1k residents (69 outlets)" },
      imd: { score: 0.7, label: "IMD deprivation score", raw: "14.5 (pop-weighted avg)" },
      pct_flats: { score: 7.5, label: "% flats (Census 2021)", raw: "62.2%" },
      pop_density: { score: 0.7, label: "Population density", raw: "46 persons/ha" },
      station_usage: { score: 2.0, label: "Station usage (TfL/NR)", raw: "4,408,040 annual entries+exits" },
    },
    kbt: "Detritus was the main issue. Leaf fall not cleared, causing related drainage and slip problems."
  },
  "Hornsey": {
    rsi: 3.3,
    indicators: {
      fixmystreet: { score: 0.6, label: "FixMyStreet reports", raw: "3.4 per 1k residents (51 total)" },
      food_outlets: { score: 3.3, label: "Food outlet density", raw: "6.5 per 1k residents (98 outlets)" },
      imd: { score: 3.3, label: "IMD deprivation score", raw: "23.4 (pop-weighted avg)" },
      pct_flats: { score: 8.4, label: "% flats (Census 2021)", raw: "66.5%" },
      pop_density: { score: 5.9, label: "Population density", raw: "110 persons/ha" },
      station_usage: { score: 0.7, label: "Station usage (TfL/NR)", raw: "1,500,360 annual entries+exits" },
    },
    kbt: null
  },
  "Muswell Hill": {
    rsi: 2.5,
    indicators: {
      fixmystreet: { score: 2.6, label: "FixMyStreet reports", raw: "9.0 per 1k residents (79 total)" },
      food_outlets: { score: 5.4, label: "Food outlet density", raw: "9.2 per 1k residents (81 outlets)" },
      imd: { score: 0.3, label: "IMD deprivation score", raw: "13.0 (pop-weighted avg)" },
      pct_flats: { score: 6.8, label: "% flats (Census 2021)", raw: "58.8%" },
      pop_density: { score: 2.6, label: "Population density", raw: "69 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: null
  },
  "Noel Park": {
    rsi: 6.4,
    indicators: {
      fixmystreet: { score: 6.2, label: "FixMyStreet reports", raw: "18.6 per 1k residents (255 total)" },
      food_outlets: { score: 10.0, label: "Food outlet density", raw: "15.2 per 1k residents (209 outlets)" },
      imd: { score: 6.4, label: "IMD deprivation score", raw: "34.0 (pop-weighted avg)" },
      pct_flats: { score: 5.2, label: "% flats (Census 2021)", raw: "51.1%" },
      pop_density: { score: 6.3, label: "Population density", raw: "115 persons/ha" },
      station_usage: { score: 3.7, label: "Station usage (TfL/NR)", raw: "7,948,900 annual entries+exits" },
    },
    kbt: "Heavy litter on side streets off the high street. KBT noted \\u2018considerably different frequencies of cleansing\\u2019 as the cause of variation between main retail area and surrounding streets."
  },
  "Northumberland Park": {
    rsi: 4.3,
    indicators: {
      fixmystreet: { score: 0.7, label: "FixMyStreet reports", raw: "3.7 per 1k residents (55 total)" },
      food_outlets: { score: 2.8, label: "Food outlet density", raw: "5.9 per 1k residents (87 outlets)" },
      imd: { score: 10.0, label: "IMD deprivation score", raw: "46.1 (pop-weighted avg)" },
      pct_flats: { score: 7.8, label: "% flats (Census 2021)", raw: "63.9%" },
      pop_density: { score: 2.6, label: "Population density", raw: "69 persons/ha" },
      station_usage: { score: 0.4, label: "Station usage (TfL/NR)", raw: "943,776 annual entries+exits" },
    },
    kbt: "Among the least favourable of all wards for every element surveyed. Massive fly-tips observed. Leeside Road had \\u2018one of the most significant fly-tips the surveyor had ever seen.\\u2019 Industrial areas severely affected."
  },
  "Seven Sisters": {
    rsi: 5.7,
    indicators: {
      fixmystreet: { score: 2.5, label: "FixMyStreet reports", raw: "8.6 per 1k residents (79 total)" },
      food_outlets: { score: 3.2, label: "Food outlet density", raw: "6.4 per 1k residents (59 outlets)" },
      imd: { score: 6.1, label: "IMD deprivation score", raw: "33.0 (pop-weighted avg)" },
      pct_flats: { score: 6.6, label: "% flats (Census 2021)", raw: "57.9%" },
      pop_density: { score: 7.9, label: "Population density", raw: "135 persons/ha" },
      station_usage: { score: 9.1, label: "Station usage (TfL/NR)", raw: "19,728,156 annual entries+exits" },
    },
    kbt: null
  },
  "South Tottenham": {
    rsi: 4.5,
    indicators: {
      fixmystreet: { score: 1.2, label: "FixMyStreet reports", raw: "5.1 per 1k residents (85 total)" },
      food_outlets: { score: 3.1, label: "Food outlet density", raw: "6.2 per 1k residents (105 outlets)" },
      imd: { score: 6.6, label: "IMD deprivation score", raw: "34.5 (pop-weighted avg)" },
      pct_flats: { score: 6.5, label: "% flats (Census 2021)", raw: "57.4%" },
      pop_density: { score: 7.5, label: "Population density", raw: "130 persons/ha" },
      station_usage: { score: 2.2, label: "Station usage (TfL/NR)", raw: "4,709,543 annual entries+exits" },
    },
    kbt: null
  },
  "St Ann's": {
    rsi: 3.6,
    indicators: {
      fixmystreet: { score: 1.5, label: "FixMyStreet reports", raw: "5.9 per 1k residents (63 total)" },
      food_outlets: { score: 0.8, label: "Food outlet density", raw: "3.2 per 1k residents (34 outlets)" },
      imd: { score: 4.5, label: "IMD deprivation score", raw: "27.4 (pop-weighted avg)" },
      pct_flats: { score: 6.0, label: "% flats (Census 2021)", raw: "55.1%" },
      pop_density: { score: 10.0, label: "Population density", raw: "161 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: null
  },
  "Stroud Green": {
    rsi: 3.1,
    indicators: {
      fixmystreet: { score: 1.1, label: "FixMyStreet reports", raw: "4.8 per 1k residents (52 total)" },
      food_outlets: { score: 1.6, label: "Food outlet density", raw: "4.4 per 1k residents (47 outlets)" },
      imd: { score: 2.4, label: "IMD deprivation score", raw: "20.1 (pop-weighted avg)" },
      pct_flats: { score: 10.0, label: "% flats (Census 2021)", raw: "74.5%" },
      pop_density: { score: 5.8, label: "Population density", raw: "109 persons/ha" },
      station_usage: { score: 0.9, label: "Station usage (TfL/NR)", raw: "2,006,957 annual entries+exits" },
    },
    kbt: null
  },
  "Tottenham Central": {
    rsi: 4.5,
    indicators: {
      fixmystreet: { score: 2.9, label: "FixMyStreet reports", raw: "9.6 per 1k residents (142 total)" },
      food_outlets: { score: 2.4, label: "Food outlet density", raw: "5.3 per 1k residents (78 outlets)" },
      imd: { score: 6.6, label: "IMD deprivation score", raw: "34.6 (pop-weighted avg)" },
      pct_flats: { score: 5.9, label: "% flats (Census 2021)", raw: "54.6%" },
      pop_density: { score: 9.0, label: "Population density", raw: "148 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: null
  },
  "Tottenham Hale": {
    rsi: 5.5,
    indicators: {
      fixmystreet: { score: 1.1, label: "FixMyStreet reports", raw: "4.8 per 1k residents (58 total)" },
      food_outlets: { score: 3.3, label: "Food outlet density", raw: "6.5 per 1k residents (79 outlets)" },
      imd: { score: 6.6, label: "IMD deprivation score", raw: "34.4 (pop-weighted avg)" },
      pct_flats: { score: 6.6, label: "% flats (Census 2021)", raw: "58.0%" },
      pop_density: { score: 6.7, label: "Population density", raw: "120 persons/ha" },
      station_usage: { score: 10.0, label: "Station usage (TfL/NR)", raw: "21,738,093 annual entries+exits" },
    },
    kbt: "Residential areas near the High Road had serious litter issues. Fly-tipping around Roseberry Avenue and Carbuncle Passage."
  },
  "West Green": {
    rsi: 3.8,
    indicators: {
      fixmystreet: { score: 2.4, label: "FixMyStreet reports", raw: "8.4 per 1k residents (125 total)" },
      food_outlets: { score: 2.6, label: "Food outlet density", raw: "5.6 per 1k residents (84 outlets)" },
      imd: { score: 6.2, label: "IMD deprivation score", raw: "33.2 (pop-weighted avg)" },
      pct_flats: { score: 5.8, label: "% flats (Census 2021)", raw: "54.1%" },
      pop_density: { score: 5.0, label: "Population density", raw: "99 persons/ha" },
      station_usage: { score: 0.0, label: "Station usage (TfL/NR)", raw: "No station in ward" },
    },
    kbt: null
  },
  "White Hart Lane": {
    rsi: 3.4,
    indicators: {
      fixmystreet: { score: 0.9, label: "FixMyStreet reports", raw: "4.3 per 1k residents (59 total)" },
      food_outlets: { score: 0.2, label: "Food outlet density", raw: "2.4 per 1k residents (34 outlets)" },
      imd: { score: 8.2, label: "IMD deprivation score", raw: "39.9 (pop-weighted avg)" },
      pct_flats: { score: 0.0, label: "% flats (Census 2021)", raw: "25.8%" },
      pop_density: { score: 5.5, label: "Population density", raw: "106 persons/ha" },
      station_usage: { score: 2.1, label: "Station usage (TfL/NR)", raw: "4,491,024 annual entries+exits" },
    },
    kbt: null
  },
  "Woodside": {
    rsi: 4.6,
    indicators: {
      fixmystreet: { score: 3.8, label: "FixMyStreet reports", raw: "12.0 per 1k residents (183 total)" },
      food_outlets: { score: 2.5, label: "Food outlet density", raw: "5.4 per 1k residents (83 outlets)" },
      imd: { score: 4.8, label: "IMD deprivation score", raw: "28.3 (pop-weighted avg)" },
      pct_flats: { score: 8.3, label: "% flats (Census 2021)", raw: "66.1%" },
      pop_density: { score: 5.3, label: "Population density", raw: "103 persons/ha" },
      station_usage: { score: 4.2, label: "Station usage (TfL/NR)", raw: "9,088,053 annual entries+exits" },
    },
    kbt: "Among the best for litter and detritus. Graffiti was a serious issue in industrial areas."
  },
};

const weights = {
  fixmystreet: 0.2,
  food_outlets: 0.15,
  imd: 0.25,
  pct_flats: 0.1,
  pop_density: 0.15,
  station_usage: 0.15,
};

const tierLabels = {
  fixmystreet: "T1",
  food_outlets: "T1",
  imd: "T1",
  pct_flats: "T2",
  pop_density: "T2",
  station_usage: "T2",
};