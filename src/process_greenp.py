import json

# Constants
SPACE_AREA_M2 = 27
DEFAULT_SHADOW_RISK = "medium"
DEFAULT_DEMAND_SCORE = 7
DEFAULT_DEMAND_LEVEL = "medium"
MIN_CAPACITY = 50  # minimum spaces to be worth building

# Load full Green P dataset
with open("data/greenp_all.json") as f:
    data = json.load(f)

carparks = data["carparks"]

locations = []
location_id = 1

for carpark in carparks:
    # Filter 1 - outdoor surface only
    if carpark["carpark_type"] != "surface":
        continue

    # Filter 2 - skip if under construction
    if carpark["is_under_construction"]:
        continue

    # Filter 3 - minimum capacity
    capacity = int(carpark["capacity"])
    if capacity < MIN_CAPACITY:
        continue

    # Calculate area
    area_m2 = capacity * SPACE_AREA_M2

    # Build location object
    location = {
        "id": location_id,
        "name": f"Green P - {carpark['address']}",
        "address": carpark["address"] + ", Toronto",
        "lat": float(carpark["lat"]),
        "lng": float(carpark["lng"]),
        "area_m2": area_m2,
        "capacity": capacity,
        "outdoor": True,
        "shadow_risk": DEFAULT_SHADOW_RISK,
        "demand_score": DEFAULT_DEMAND_SCORE,
        "demand_level": DEFAULT_DEMAND_LEVEL,
        "neighbourhood": "Toronto",
        "rating": "pending"
    }

    locations.append(location)
    location_id += 1

# Sort by area largest first
locations.sort(key=lambda x: x["area_m2"], reverse=True)

# Save
with open("data/locations_auto.json", "w") as f:
    json.dump(locations, f, indent=4)

print(f"Found {len(locations)} surface Green P lots with 50+ spaces")
print(f"\nTop 10 by area:")
for loc in locations[:10]:
    print(f"  {loc['name']} — {loc['area_m2']:,} m² ({loc['capacity']} spaces)")