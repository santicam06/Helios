import json

# Constants
PANEL_SIZE_M2 = 2
PANEL_WATT = 400
PEAK_SUN_HOURS = 4
DAYS_PER_YEAR = 365
ELECTRICITY_PRICE = 0.13
INSTALL_COST_PER_M2 = 500
USABLE_AREA_RATIO = 0.70

def calculate_location(location):
    usable_area = location["area_m2"] * USABLE_AREA_RATIO
    num_panels = usable_area / PANEL_SIZE_M2
    energy_kwh = num_panels * (PANEL_WATT/1000) * PEAK_SUN_HOURS * DAYS_PER_YEAR
    revenue = energy_kwh * ELECTRICITY_PRICE
    install_cost = usable_area * INSTALL_COST_PER_M2
    payback_years = install_cost / revenue
    solar_score = revenue * 0.70
    demand_score = location["demand_score"] * 10000 * 0.30
    final_score = solar_score + demand_score

    return {
        "id": location["id"],
        "name": location["name"],
        "lat": location["lat"],
        "lng": location["lng"],
        "address": location["address"],
        "neighbourhood": location["neighbourhood"],
        "area_m2": location["area_m2"],
        "usable_area": round(usable_area),
        "num_panels": round(num_panels),
        "energy_kwh_year": round(energy_kwh),
        "revenue_year": round(revenue),
        "install_cost": round(install_cost),
        "payback_years": round(payback_years, 1),
        "demand_score": location["demand_score"],
        "final_score": round(final_score)
    }

# Load locations
with open("data/locations_auto.json") as f:
    locations = json.load(f)

# Calculate all locations
results = []
for location in locations:
    result = calculate_location(location)
    results.append(result)
    print(f"{result['name']}: Revenue ${result['revenue_year']:,}/yr | Payback {result['payback_years']} years | Score {result['final_score']:,}")

# Sort by final score
results.sort(key=lambda x: x["final_score"], reverse=True)

# Save results
with open("data/results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nTop locations saved to data/results.json")