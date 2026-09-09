import json

def calculate_averages():
    json_path = r"C:\Users\camac\OneDrive\Desktop\Programming\Projects Santiago\Helios\data\results.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    energy_list = [item['energy_kwh_year'] for item in data if 'energy_kwh_year' in item]
    revenue_list = [item['revenue_year'] for item in data if 'revenue_year' in item]
    
    avg_energy = sum(energy_list) / len(energy_list) if energy_list else 0
    avg_revenue = sum(revenue_list) / len(revenue_list) if revenue_list else 0
    
    print(f"Average Energy (kWh/year): {avg_energy:.2f}")
    print(f"Average Revenue ($/year): {avg_revenue:.2f}")
    print(f"Total parkings: {len(data)}")

if __name__ == "__main__":
    calculate_averages()
