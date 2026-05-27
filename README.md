# Helios 🌞

A geographic analysis tool that identifies the top potential Green P parking locations 
in Toronto for solar panel installation.

<a href="https://helios-tool.vercel.app/"> <img width="640" height="367" alt="Image" src="https://github.com/user-attachments/assets/de497214-8514-454d-85ca-f30634237771" /> </a>

## What it does
- Analyzes all 104 surface Green P parking lots in Toronto
- Calculates solar energy potential based on lot size and Toronto sun data
- Estimates installation cost and yearly revenue
- Calculates payback period for each location
- Shows all locations on an interactive map scored by investment return

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






## Data sources
- Green P locations: Toronto Open Data
- Solar radiation: Toronto average 4 peak sun hours/day (NRCan)
- Electricity price: Ontario average $0.13/kWh

## Scoring formula
