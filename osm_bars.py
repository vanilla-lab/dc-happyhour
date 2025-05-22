import requests
import json

# Overpass query for bars in Washington, D.C.
overpass_url = "https://overpass-api.de/api/interpreter"
overpass_query = """
[out:json][timeout:25];
area["name"="District of Columbia"]["boundary"="administrative"]["admin_level"="6"]->.searchArea;
(
  node["amenity"="bar"](area.searchArea);
  way["amenity"="bar"](area.searchArea);
  relation["amenity"="bar"](area.searchArea);
);
out center;
"""

response = requests.post(overpass_url, data={"data": overpass_query})

if response.status_code == 200:
    data = response.json()
    # Save just useful info (like name + lat/lon)
    bars = []
    for element in data["elements"]:
        name = element["tags"].get("name", "Unnamed Bar")
        if "lat" in element:
            lat, lon = element["lat"], element["lon"]
        elif "center" in element:
            lat, lon = element["center"]["lat"], element["center"]["lon"]
        else:
            continue
        bars.append({"name": name, "lat": lat, "lon": lon})

    with open("bars.json", "w") as f:
        json.dump(bars, f, indent=2)

    print("✅ bars.json saved.")
else:
    print(f"❌ Failed with status code: {response.status_code}")
