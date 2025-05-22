import requests
import json

# Updated Overpass query using correct area ID for DC
# We find DC by looking up by relation and use that ID
query = """
[out:json][timeout:25];
// Washington DC relation ID (global)
area["ISO3166-2"="US-DC"]->.searchArea;
(
  node["amenity"="bar"](area.searchArea);
  way["amenity"="bar"](area.searchArea);
  relation["amenity"="bar"](area.searchArea);
);
out center;
"""

url = "https://overpass-api.de/api/interpreter"
response = requests.post(url, data={'data': query})

if response.status_code == 200:
    data = response.json()
    bars = []
    for el in data['elements']:
        name = el['tags'].get('name')
        lat = el.get('lat') or el.get('center', {}).get('lat')
        lon = el.get('lon') or el.get('center', {}).get('lon')
        if name and lat and lon:
            bars.append({
                'name': name,
                'lat': lat,
                'lng': lon
            })

    with open('bars.json', 'w') as f:
        json.dump(bars, f, indent=2)
    print(f"✅ Saved {len(bars)} bars to bars.json")
else:
    print(f"❌ Failed with status code: {response.status_code}")
