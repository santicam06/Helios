# Helios 🌞

A GIS-based solar infrastructure planning tool that identifies the best Green P parking lots in Toronto for solar panel installation — combining solar energy potential with neighbourhood electricity demand.

<a href="https://helios-tool.vercel.app/"> <img width="640" height="367" alt="Image" src="https://github.com/user-attachments/assets/de497214-8514-454d-85ca-f30634237771" /> </a>

## What it does

- Automatically filters 104 surface Green P lots from Toronto's Open Data
- Calculates solar energy potential based on lot area and Toronto sun data
- Estimates annual revenue, installation cost, and payback period per location
- Scores each location using a weighted formula: 70% solar revenue + 30% neighbourhood demand
- Visualizes all locations on an interactive GIS map with color-coded markers and demand heatmap
- Ranked sidebar listing all 104 locations by energy output
- Click any location to fly to it and view full financial breakdown

## Scoring formula

```
Score = (Revenue × 0.70) + (Demand Score × 10,000 × 0.30)

Revenue = usable_area × panels × sun_hours × electricity_price
Usable area = capacity × 27m² × 0.70
Solar panels: 400W per 2m²
Peak sun hours: 4/day (Toronto average — NRCan)
Electricity price: $0.13/kWh (Ontario average)
Installation cost: $500/m²
```

## Map legend

| Color | Meaning |
|-------|---------|
| 🟢 Green | Excellent — score 300k+ |
| 🟠 Orange | Good — score 100k–300k |
| 🔴 Red | Lower priority — score <100k |
| 🔵 Blue heatmap | High electricity demand zone |

## How to run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Process all Green P locations
```bash
python3 src/process_greenp.py
```

### 3. Calculate scores
```bash
python3 src/calculate.py
```

### 4. Generate map
```bash
python3 src/create_map.py
```

### 5. Open map
Open `output/map.html` in your browser.

## Project structure

```
Helios/
├── data/
│   ├── greenp_all.json        # Raw Toronto Open Data
│   ├── locations_auto.json    # 104 filtered surface lots
│   └── results.json           # Scored and ranked results
├── src/
│   ├── process_greenp.py      # Filters and processes raw data
│   ├── calculate.py           # Scoring algorithm
│   └── create_map.py          # Generates interactive map
├── output/
│   └── map.html               # Final interactive map
└── index.html                 # Landing page
```

## Data sources

- Green P locations: [Toronto Open Data](https://open.toronto.ca/dataset/green-p-parking/)
- Solar radiation: Toronto average 4 peak sun hours/day (NRCan)
- Electricity price: Ontario average $0.13/kWh
- Demand zones: 10 high-consumption neighbourhoods identified from Toronto density data

## Key results

| Metric | Value |
|--------|-------|
| Locations analyzed | 104 surface Green P lots |
| Top location | Green P - 2800 Steeles Ave W |
| Top revenue/year | $1,350,000 |
| Average payback | ~13 years |
| Homes powered (top 6) | 8,600+ annually |
| Land cost | $0 (city-owned) |

## Team

Santiago Camacho Moyana · Nareen Ibrahim · Dogukan Bakibaba

Seneca Polytechnic Hackathon 2026 — Theme 1: Clean Energy Generation and Integration
