import json
import math
import folium
from folium.plugins import MarkerCluster, HeatMap

# Load results
with open("data/results.json") as f:
    locations = json.load(f)

# Color function based on final score
def get_color(final_score):
    if final_score >= 300000:
        return "#2ecc71"  # green
    elif final_score >= 100000:
        return "#f39c12"  # orange
    else:
        return "#e74c3c"  # red

# Marker size based on score
def get_radius(final_score):
    if final_score >= 300000:
        return 20
    elif final_score >= 100000:
        return 14
    else:
        return 9

# Dynamic reasons based on real data
def get_reasons(loc):
    reasons = []
    if loc["area_m2"] >= 15000:
        reasons.append("Very large lot — maximum energy output")
    elif loc["area_m2"] >= 8000:
        reasons.append("Large lot area — high energy output")
    if loc["demand_score"] >= 8:
        reasons.append("High neighbourhood energy demand")
    elif loc["demand_score"] >= 6:
        reasons.append("Moderate neighbourhood demand")
    if loc["revenue_year"] >= 500000:
        reasons.append("Excellent revenue potential")
    elif loc["revenue_year"] >= 200000:
        reasons.append("Strong revenue potential")
    if loc["final_score"] >= 300000:
        reasons.append("Top investment opportunity")
    if not reasons:
        reasons.append("Lower priority — consider larger locations first")
    return reasons

# Create map centered on Toronto
m = folium.Map(
    location=[43.6450, -79.3900],
    zoom_start=12,
    tiles="CartoDB positron"
)

# Demand hotspots data
demand_hotspots = [
    {"name": "Downtown Core",           "lat": 43.6532, "lng": -79.3832, "intensity": 0.95},
    {"name": "North York Centre",       "lat": 43.7615, "lng": -79.4111, "intensity": 0.85},
    {"name": "Scarborough Town Centre", "lat": 43.7764, "lng": -79.2318, "intensity": 0.80},
    {"name": "Etobicoke Centre",        "lat": 43.6205, "lng": -79.5132, "intensity": 0.75},
    {"name": "York Mills",              "lat": 43.7445, "lng": -79.4009, "intensity": 0.70},
    {"name": "Finch & Jane",            "lat": 43.7574, "lng": -79.5197, "intensity": 0.75},
    {"name": "Kennedy & Eglinton",      "lat": 43.7320, "lng": -79.2630, "intensity": 0.70},
    {"name": "Danforth",                "lat": 43.6773, "lng": -79.3498, "intensity": 0.72},
    {"name": "Liberty Village",         "lat": 43.6420, "lng": -79.4150, "intensity": 0.78},
    {"name": "Weston",                  "lat": 43.7070, "lng": -79.5290, "intensity": 0.65},
]

def expand_hotspot(name, lat, lng, intensity, count=15, spread=0.025):
    points = [[lat, lng, intensity]]  # center
    # inner ring
    for i in range(count):
        angle = (360 / count) * i
        dlat = (spread * 0.4) * math.cos(math.radians(angle))
        dlng = (spread * 0.4) * math.sin(math.radians(angle))
        points.append([lat + dlat, lng + dlng, intensity * 0.85])
    # outer ring
    for i in range(count):
        angle = (360 / count) * i
        dlat = spread * math.cos(math.radians(angle))
        dlng = spread * math.sin(math.radians(angle))
        points.append([lat + dlat, lng + dlng, intensity * 0.5])
    return points

# Build heatmap data
heat_data = []
for h in demand_hotspots:
    heat_data.extend(expand_hotspot(h["name"], h["lat"], h["lng"], h["intensity"]))

# Add HeatMap layer — blue/cyan gradient only
HeatMap(
    heat_data,
    radius=59,
    blur=40,
    min_opacity=0.2,
    gradient={0.0: "#003366", 0.5: "#0066cc", 0.8: "#00ccff", 1.0: "#00ffff"}
).add_to(m)

# MarkerCluster — disable clustering when zoomed in close
cluster = MarkerCluster(disableClusteringAtZoom=13).add_to(m)

# Add markers
for i, loc in enumerate(locations):
    reasons = get_reasons(loc)
    reasons_html = "".join([f"• {r}<br>" for r in reasons])

    popup_html = f"""
    <div style="width:270px; font-family:Arial; padding:5px">
        <h3 style="color:#2c7a2c; margin-bottom:8px">{loc['name']}</h3>
        <table style="width:100%; font-size:13px">
            <tr><td><b>Area</b></td><td>{loc['area_m2']:,} m²</td></tr>
            <tr><td><b>Solar Panels</b></td><td>{loc['num_panels']:,}</td></tr>
            <tr><td><b>Energy/Year</b></td><td>{loc['energy_kwh_year']:,} kWh</td></tr>
            <tr><td><b>Revenue/Year</b></td><td>${loc['revenue_year']:,}</td></tr>
            <tr><td><b>Install Cost</b></td><td>${loc['install_cost']:,}</td></tr>
            <tr><td><b>Payback</b></td><td>{loc['payback_years']} years</td></tr>
            <tr><td><b>Demand Score</b></td><td>{loc['demand_score']}/10</td></tr>
        </table>
        <hr>
        <b style="font-size:12px">Why this location?</b><br>
        <span style="font-size:12px; color:#555">{reasons_html}</span>
        <hr>
        <b style="color:#2c7a2c; font-size:14px">Score: {loc['final_score']:,}</b>
    </div>
    """

    folium.CircleMarker(
        location=[loc["lat"], loc["lng"]],
        radius=get_radius(loc['final_score']),
        color=get_color(loc['final_score']),
        fill=True,
        fill_color=get_color(loc['final_score']),
        fill_opacity=0.85,
        weight=2,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"#{i+1} {loc['name']} | ${loc['revenue_year']:,}/yr"
    ).add_to(cluster)

# Sort locations by energy yield descending for the sidebar list
locations_sorted = sorted(locations, key=lambda x: x['energy_kwh_year'], reverse=True)

# Generate sidebar list items HTML
list_items_html = ""
for loc in locations_sorted:
    list_items_html += f"""
    <div class="list-item" onclick="zoomToLocation({loc['lat']}, {loc['lng']})">
        <div class="item-name">{loc['name']}</div>
        <div class="item-stats">{loc['energy_kwh_year']:,} kWh/year</div>
    </div>
    """

# UI elements — sidebar, legend, dropdown, home button
ui_html = f"""
<style>
    .map-legend {{
        position: fixed;
        bottom: 30px;
        left: 30px;
        z-index: 1000;
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #ccc;
        font-family: Arial;
        font-size: 13px;
    }}
    .sidebar {{
        position: fixed;
        top: 20px;
        bottom: 30px;
        right: -350px;
        width: 320px;
        background-color: white;
        z-index: 2000;
        transition: right 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        font-family: Arial, sans-serif;
        border-radius: 8px;
        border: 2px solid #ccc;
        overflow: hidden;
    }}
    .leaflet-interactive:focus {{
        outline: none !important;
    }}
    .highlighted-marker {{
        filter: drop-shadow(0 0 5px gold);
    }}
    .sidebar.open {{
        right: 20px;
    }}
    .sidebar-header {{
        padding: 15px;
        background-color: #2c7a2c;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }}
    .sidebar-content {{
        flex: 1;
        overflow-y: auto;
        padding: 10px;
    }}
    .list-item {{
        padding: 12px;
        border-bottom: 1px solid #eee;
        cursor: pointer;
        transition: background-color 0.2s;
    }}
    .list-item:hover {{
        background-color: #f9f9f9;
    }}
    .item-name {{
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
    }}
    .item-stats {{
        font-size: 12px;
        color: #666;
    }}
    .custom-dropdown {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1001;
    }}
    .dropdown-btn {{
        background-color: white;
        border: 2px solid rgba(0,0,0,0.2);
        border-radius: 4px;
        width: 40px;
        height: 40px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 5px rgba(0,0,0,0.4);
        color: black;
    }}
    .dropdown-btn:hover {{
        background-color: #f4f4f4;
        color: #0078A8;
    }}
    .close-btn {{
        position: absolute;
        right: 15px;
        cursor: pointer;
        font-size: 24px;
        line-height: 1;
    }}
    .home-control {{
        position: fixed;
        top: 80px;
        left: 10px;
        z-index: 1000;
    }}
    .home-btn {{
        background-color: white;
        border: 2px solid rgba(0,0,0,0.2);
        border-radius: 4px;
        width: 34px;
        height: 34px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 5px rgba(0,0,0,0.4);
        text-decoration: none;
        color: black;
    }}
    .home-btn:hover {{
        background-color: #f4f4f4;
        color: #0078A8;
    }}
</style>

<div class="sidebar" id="locationSidebar">
    <div class="sidebar-header">
        <h3 style="margin:0; font-size:18px">Solar Potential</h3>
        <span class="close-btn" onclick="toggleSidebar()">&times;</span>
    </div>
    <div class="sidebar-content">
        {list_items_html}
    </div>
</div>

<div class="map-legend">
    <b>Solar Opportunity Score</b><br><br>
    <span style="color:#2ecc71">●</span> Excellent (300k+)<br>
    <span style="color:#f39c12">●</span> Good (100k - 300k)<br>
    <span style="color:#e74c3c">●</span> Lower Priority (&lt;100k)<br>
    <br>
    <b>Electricity Demand</b><br>
    <span style="color:#00ffff">●</span> High demand zone<br>
    <br>
    <small style="font-size: 13px;">Bigger circle = better investment</small>
</div>

<div class="custom-dropdown">
    <button class="dropdown-btn" onclick="toggleSidebar()">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <circle cx="3" cy="6" r="1"></circle>
            <circle cx="3" cy="12" r="1"></circle>
            <circle cx="3" cy="18" r="1"></circle>
        </svg>
    </button>
</div>

<div class="home-control">
    <a href="../index.html" class="home-btn" title="Go Home">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
    </a>
</div>

<script>
    var currentHighlight = null;

    window.addEventListener('load', function() {{
        var map_element = document.querySelector('.folium-map');
        var map_id = map_element.id;
        var map_instance = window[map_id];

        map_instance.eachLayer(function(layer) {{
            if (layer.options && layer.options.radius) {{
                layer.on('click', function(e) {{
                    highlightAndZoom(e.target, e.target.getLatLng().lat, e.target.getLatLng().lng);
                }});
            }}
        }});
    }});

    function toggleSidebar() {{
        document.getElementById('locationSidebar').classList.toggle('open');
    }}

    function highlightAndZoom(layer, lat, lng) {{
        var map_element = document.querySelector('.folium-map');
        var map_id = map_element.id;
        var map_instance = window[map_id];

        map_instance.flyTo([lat, lng], 16);

        if (currentHighlight && currentHighlight !== layer) {{
            currentHighlight.setStyle({{
                weight: 2,
                color: currentHighlight.options.originalColor || currentHighlight.options.color
            }});
        }}

        if (!layer.options.originalColor) {{
            layer.options.originalColor = layer.options.color;
        }}

        layer.setStyle({{ weight: 5, color: '#FFD700' }});
        currentHighlight = layer;
        layer.bringToFront();
    }}

    function zoomToLocation(lat, lng) {{
        var map_element = document.querySelector('.folium-map');
        var map_id = map_element.id;
        var map_instance = window[map_id];

        map_instance.eachLayer(function(layer) {{
            if (layer.options && layer.options.radius) {{
                var latlng = layer.getLatLng();
                if (Math.abs(latlng.lat - lat) < 0.00001 && Math.abs(latlng.lng - lng) < 0.00001) {{
                    highlightAndZoom(layer, lat, lng);
                }}
            }}
        }});

        if (window.innerWidth < 768) {{
            toggleSidebar();
        }}
    }}
</script>
"""

m.get_root().html.add_child(folium.Element(ui_html))

# Save map
with open("output/map.html", "w", encoding="utf-8") as f:
    f.write(m.get_root().render())
print("Map saved to output/map.html")