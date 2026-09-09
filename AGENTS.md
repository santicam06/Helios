# Helios 🌞

## Project Overview
Helios is a geographic analysis tool designed to identify optimal locations for solar panel installations on Green P surface parking lots in Toronto. It processes data on lot sizes and solar potential to calculate financial viability, including installation costs, yearly revenue, and payback periods.

## Architecture
- **Data Layer**: JSON files stored in `data/` containing raw and processed location and scoring information.
- **Processing Layer**: Python scripts in `src/` perform data ingestion, scoring, and visualization.
- **Output Layer**: An interactive map generated in `output/map.html`.

## Key Commands
- **Install Dependencies**: `pip install -r requirements.txt`
- **Process Data**: `python3 src/process_greenp.py`
- **Calculate Scores**: `python3 src/calculate.py`
- **Generate Map**: `python3 src/create_map.py`

## Development Conventions
- Use standard Python 3.x.
- Keep dependencies updated in `requirements.txt`.
- Data transformation logic should be kept in the `src/` directory.
- Always verify outputs in the `output/` directory before finalizing changes.
