import json
import folium

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

# Create map centered on Toronto
m = folium.Map(
    location=[43.6450, -79.3900],
    zoom_start=12,
    tiles="CartoDB positron"
)

# Add markers
for loc in locations:
    popup_html = f"""
    <div style="width:260px; font-family:Arial; padding:5px">
        <h3 style="color:#2c7a2c; margin-bottom:8px">{loc['name']}</h3>
        <table style="width:100%; font-size:13px">
            <tr><td><b>Neighbourhood</b></td><td>{loc['neighbourhood']}</td></tr>
            <tr><td><b>Area</b></td><td>{loc['area_m2']:,} m²</td></tr>
            <tr><td><b>Solar Panels</b></td><td>{loc['num_panels']:,}</td></tr>
            <tr><td><b>Energy/Year</b></td><td>{loc['energy_kwh_year']:,} kWh</td></tr>
            <tr><td><b>Revenue/Year</b></td><td>${loc['revenue_year']:,}</td></tr>
            <tr><td><b>Install Cost</b></td><td>${loc['install_cost']:,}</td></tr>
            <tr><td><b>Payback</b></td><td>{loc['payback_years']} years</td></tr>
            <tr><td><b>Demand Score</b></td><td>{loc['demand_score']}/10</td></tr>
        </table>
        <hr>
        <b style="color:#2c7a2c; font-size:14px">Score: {loc['final_score']:,}</b>
    </div>
    """
    folium.CircleMarker(
        location=[loc["lat"], loc["lng"]],
        radius=get_radius(loc["final_score"]),
        color=get_color(loc["final_score"]),
        fill=True,
        fill_color=get_color(loc["final_score"]),
        fill_opacity=0.85,
        weight=2,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"#{locations.index(loc)+1} {loc['name']} | ${loc['revenue_year']:,}/yr"
    ).add_to(m)

# Add legend
legend_html = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
     background-color: white; padding: 15px; border-radius: 8px;
     border: 2px solid #ccc; font-family: Arial; font-size: 13px">
    <b>Solar Opportunity Score</b><br><br>
    <span style="color:#2ecc71">●</span> Excellent (300k+)<br>
    <span style="color:#f39c12">●</span> Good (100k - 300k)<br>
    <span style="color:#e74c3c">●</span> Lower Priority (&lt;100k)<br>
    <br>
    <small>Bigger circle = better investment</small>
</div>
"""

dropdown_html = """
<style>
    .custom-dropdown {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1001;
    }
    .dropdown-btn {
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
    }
    .dropdown-btn:hover {
        background-color: #f4f4f4;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        right: 0;
        top: 40px;
        background-color: white;
        min-width: 160px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        border-radius: 4px;
        padding: 8px 0;
        border: 1px solid #ccc;
    }
    .dropdown-content a {
        color: black;
        padding: 8px 16px;
        text-decoration: none;
        display: block;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    .dropdown-content a:hover {
        background-color: #f1f1f1;
    }
    .show { display: block; }
</style>

<div class="custom-dropdown">
    <button onclick="toggleDropdown()" class="dropdown-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <circle cx="3" cy="6" r="1"></circle>
            <circle cx="3" cy="12" r="1"></circle>
            <circle cx="3" cy="18" r="1"></circle>
        </svg>
    </button>
    <div id="myDropdown" class="dropdown-content">
        <a href="../index.html">🏠 Home</a>
        <a href="https://github.com/" target="_blank">💻 Source Code</a>
        <a href="mailto:info@helios.com">📧 Contact Us</a>
    </div>
</div>

<script>
    function toggleDropdown() {
        document.getElementById("myDropdown").classList.toggle("show");
    }

    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
        if (!event.target.matches('.dropdown-btn') && !event.target.closest('.dropdown-btn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }
</script>
"""

m.get_root().add_child(folium.Element(legend_html))
m.get_root().add_child(folium.Element(dropdown_html))

# Save map with explicit UTF-8 encoding
with open("output/map.html", "w", encoding="utf-8") as f:
    f.write(m.get_root().render())
print("Map saved to output/map.html with UTF-8 encoding.")