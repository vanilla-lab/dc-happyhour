import requests
import json
import time
from typing import List, Dict, Optional

class GooglePlacesBars:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://places.googleapis.com/v1"
        
    def search_bars(self, location: str = "Washington, DC", radius: int = 50000) -> List[Dict]:
        """
        Search for bars in the specified location using Google Places API (New)
        """
        search_url = f"{self.base_url}/places:searchText"
        
        # For the new API, we need to use POST with a JSON body
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.displayName,places.id,places.location,places.rating,places.userRatingCount,places.priceLevel,places.types,places.formattedAddress'
        }
        
        body = {
            'textQuery': 'bars in Washington DC',
            'maxResultCount': 20,
            'locationBias': {
                'circle': {
                    'center': {
                        'latitude': 38.9072,
                        'longitude': -77.0369
                    },
                    'radius': radius
                }
            }
        }
        
        bars = []
        
        try:
            response = requests.post(search_url, headers=headers, json=body)
            
            if response.status_code != 200:
                print(f"❌ API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return bars
                
            data = response.json()
            
            # Process results
            for place in data.get('places', []):
                bar_info = self._extract_bar_info_new(place)
                if bar_info:
                    bars.append(bar_info)
            
            print(f"✅ Found {len(bars)} bars from API")
            
        except Exception as e:
            print(f"❌ Error during API request: {e}")
        
        return bars
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information for a specific place (New API format)
        """
        details_url = f"{self.base_url}/places/{place_id}"
        
        headers = {
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'displayName,formattedAddress,internationalPhoneNumber,rating,userRatingCount,regularOpeningHours,websiteUri,priceLevel,types'
        }
        
        response = requests.get(details_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        
        return None
    
    def _extract_bar_info_new(self, place: Dict) -> Optional[Dict]:
        """
        Extract relevant information from a place result (New API format)
        """
        try:
            # Basic info
            bar_info = {
                'name': place.get('displayName', {}).get('text', 'Unnamed Bar'),
                'place_id': place.get('id'),
                'lat': place.get('location', {}).get('latitude'),
                'lng': place.get('location', {}).get('longitude'),
                'rating': place.get('rating'),
                'user_ratings_total': place.get('userRatingCount'),
                'price_level': place.get('priceLevel'),
                'types': place.get('types', []),
                'formatted_address': place.get('formattedAddress')
            }
            
            # Only include bars with valid coordinates
            if bar_info['lat'] and bar_info['lng']:
                return bar_info
            return None
            
        except Exception as e:
            print(f"❌ Error extracting bar info: {e}")
            return None

    def _extract_bar_info(self, place: Dict) -> Optional[Dict]:
        """
        Extract relevant information from a place result (Legacy API format)
        """
        try:
            # Basic info
            bar_info = {
                'name': place.get('name', 'Unnamed Bar'),
                'place_id': place.get('place_id'),
                'lat': place.get('geometry', {}).get('location', {}).get('lat'),
                'lng': place.get('geometry', {}).get('location', {}).get('lng'),
                'rating': place.get('rating'),
                'user_ratings_total': place.get('user_ratings_total'),
                'price_level': place.get('price_level'),
                'types': place.get('types', []),
                'formatted_address': place.get('formatted_address')
            }
            
            # Only include bars with valid coordinates
            if bar_info['lat'] and bar_info['lng']:
                return bar_info
            return None
            
        except Exception as e:
            print(f"❌ Error extracting bar info: {e}")
            return None
    
    def enrich_bars_with_details(self, bars: List[Dict]) -> List[Dict]:
        """
        Enrich basic bar info with detailed place information
        """
        enriched_bars = []
        
        for i, bar in enumerate(bars):
            print(f"📊 Enriching bar {i+1}/{len(bars)}: {bar['name']}")
            
            if bar.get('place_id'):
                details = self.get_place_details(bar['place_id'])
                if details:
                    # Merge details with basic info
                    bar.update({
                        'phone': details.get('internationalPhoneNumber'),
                        'website': details.get('websiteUri'),
                        'opening_hours': details.get('regularOpeningHours', {}).get('weekdayDescriptions', []),
                        'price_level': details.get('priceLevel'),
                        'types': details.get('types', [])
                    })
            
            enriched_bars.append(bar)
            
            # Rate limiting - be nice to Google's API
            time.sleep(0.1)
        
        return enriched_bars

def main():
    # You'll need to get an API key from Google Cloud Console
    # https://console.cloud.google.com/apis/credentials
    API_KEY = "AIzaSyBcAFMGC3fTZ1-RdAtAWF5WfcCcRWAaPl8"
    
    if not API_KEY or API_KEY == "YOUR_GOOGLE_PLACES_API_KEY_HERE":
        print("❌ Please set your Google Places API key in the script")
        print("📝 Get one from: https://console.cloud.google.com/apis/credentials")
        return
    
    # Initialize the scraper
    scraper = GooglePlacesBars(API_KEY)
    
    print("🔍 Searching for bars in Washington, DC...")
    
    # Search for bars
    bars = scraper.search_bars("Washington, DC", radius=50000)
    
    if not bars:
        print("❌ No bars found")
        return
    
    print(f"✅ Found {len(bars)} bars")
    
    # Enrich with detailed information
    print("📊 Enriching bar information...")
    enriched_bars = scraper.enrich_bars_with_details(bars)
    
    # Save to file
    output_file = "bars_google.json"
    with open(output_file, "w") as f:
        json.dump(enriched_bars, f, indent=2)
    
    print(f"✅ Saved {len(enriched_bars)} bars to {output_file}")
    
    # Show sample of what we got
    if enriched_bars:
        sample = enriched_bars[0]
        print(f"\n📋 Sample bar data:")
        print(f"   Name: {sample['name']}")
        print(f"   Address: {sample.get('formatted_address', 'N/A')}")
        print(f"   Rating: {sample.get('rating', 'N/A')}")
        print(f"   Phone: {sample.get('phone', 'N/A')}")
        print(f"   Website: {sample.get('website', 'N/A')}")

if __name__ == "__main__":
    main()
