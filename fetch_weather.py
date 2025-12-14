"""
Weather Data Fetcher
Downloads and parses weather data from Taiwan Central Weather Administration (CWA) API
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional


# CWA API Configuration
API_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001"
API_KEY = "CWA-0F33C0B7-CF31-4D97-9034-2D468ED87ABC"

# Region mapping for Taiwan locations
REGION_MAP = {
    # 北部 (North)
    '臺北': '北部', '新北': '北部', '基隆': '北部', '桃園': '北部', 
    '新竹': '北部', '宜蘭': '北部',
    # 中部 (Central)
    '苗栗': '中部', '臺中': '中部', '彰化': '中部', '南投': '中部', '雲林': '中部',
    # 南部 (South)
    '嘉義': '南部', '臺南': '南部', '高雄': '南部', '屏東': '南部',
    # 東部 (East)
    '花蓮': '東部', '臺東': '東部',
    # 離島 (Islands)
    '澎湖': '離島', '金門': '離島', '連江': '離島',
}


def get_region(location: str) -> str:
    """
    Determine the region for a given location
    
    Args:
        location: Location name
        
    Returns:
        Region name (北部/中部/南部/東部/離島)
    """
    for key, region in REGION_MAP.items():
        if key in location:
            return region
    return '其他'


def fetch_weather_data() -> Optional[Dict]:
    """
    Fetch weather data from CWA API
    
    Returns:
        JSON data from API or None if request fails
    """
    try:
        params = {
            'Authorization': API_KEY,
            'downloadType': 'WEB',
            'format': 'JSON'
        }
        
        print(f"Fetching weather data from CWA API...")
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"[OK] Successfully fetched weather data")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error fetching weather data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error parsing JSON data: {e}")
        return None


def parse_weather_data(data: Dict) -> List[Dict]:
    """
    Parse weather data and extract relevant information
    
    Args:
        data: Raw JSON data from API
        
    Returns:
        List of weather records with location, temperature, and description
    """
    weather_records = []
    
    try:
        # Navigate through the JSON structure
        # The structure may vary, so we'll handle it flexibly
        cwaopendata = data.get('cwaopendata', {})
        dataset = cwaopendata.get('dataset', {})
        
        # Try to find location data
        locations = dataset.get('location', [])
        if not locations:
            # Alternative structure
            locations = dataset.get('locations', {}).get('location', [])
        
        print(f"Found {len(locations)} locations")
        
        for location in locations:
            location_name = location.get('locationName', 'Unknown')
            region = get_region(location_name)
            
            # Extract weather elements
            weather_elements = location.get('weatherElement', [])
            
            # Initialize temperature variables
            min_temp = None
            max_temp = None
            current_temp = None
            description = None
            forecast_time = None
            
            for element in weather_elements:
                element_name = element.get('elementName', '')
                
                # Extract temperature data
                if 'MinT' in element_name or '最低溫' in element_name:
                    time_data = element.get('time', [])
                    if time_data:
                        min_temp = time_data[0].get('parameter', {}).get('parameterName')
                        if not forecast_time:
                            forecast_time = time_data[0].get('startTime')
                
                elif 'MaxT' in element_name or '最高溫' in element_name:
                    time_data = element.get('time', [])
                    if time_data:
                        max_temp = time_data[0].get('parameter', {}).get('parameterName')
                
                elif 'T' == element_name or '溫度' in element_name:
                    time_data = element.get('time', [])
                    if time_data:
                        current_temp = time_data[0].get('parameter', {}).get('parameterName')
                
                elif 'Wx' in element_name or '天氣' in element_name:
                    time_data = element.get('time', [])
                    if time_data:
                        description = time_data[0].get('parameter', {}).get('parameterName')
            
            # Convert temperature strings to floats
            try:
                min_temp = float(min_temp) if min_temp else None
            except (ValueError, TypeError):
                min_temp = None
            
            try:
                max_temp = float(max_temp) if max_temp else None
            except (ValueError, TypeError):
                max_temp = None
            
            try:
                current_temp = float(current_temp) if current_temp else None
            except (ValueError, TypeError):
                # If no current temp, use average of min/max
                if min_temp and max_temp:
                    current_temp = (min_temp + max_temp) / 2
                current_temp = None
            
            # Create weather record
            record = {
                'location': location_name,
                'region': region,
                'min_temp': min_temp,
                'max_temp': max_temp,
                'current_temp': current_temp,
                'description': description or '未提供',
                'forecast_time': forecast_time or datetime.now().isoformat()
            }
            
            weather_records.append(record)
            print(f"  [OK] {location_name} ({region}): {min_temp}°C - {max_temp}°C")
        
        print(f"\n[OK] Parsed {len(weather_records)} weather records")
        return weather_records
        
    except Exception as e:
        print(f"[ERROR] Error parsing weather data: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """
    Main function to test the weather data fetcher
    """
    print("=" * 60)
    print("Weather Data Fetcher - CWA API")
    print("=" * 60)
    
    # Fetch data
    data = fetch_weather_data()
    
    if data:
        # Parse data
        records = parse_weather_data(data)
        
        if records:
            print(f"\n{'='*60}")
            print(f"Sample Records:")
            print(f"{'='*60}")
            for record in records[:5]:
                print(f"Location: {record['location']}")
                print(f"Region: {record['region']}")
                print(f"Temperature: {record['min_temp']}°C - {record['max_temp']}°C")
                print(f"Description: {record['description']}")
                print(f"-" * 60)
        else:
            print("No records parsed")
    else:
        print("Failed to fetch data")


if __name__ == "__main__":
    main()
