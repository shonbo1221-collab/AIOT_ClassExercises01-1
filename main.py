"""
Main Pipeline Script
Orchestrates the complete weather data pipeline: fetch → parse → store
"""

import fetch_weather
import database


def main():
    """
    Execute the complete weather data pipeline
    """
    print("=" * 60)
    print("Weather Data Pipeline")
    print("=" * 60)
    
    # Step 1: Initialize database
    print("\n[1/3] Initializing database...")
    database.init_database()
    
    # Step 2: Fetch and parse weather data
    print("\n[2/3] Fetching weather data from CWA API...")
    data = fetch_weather.fetch_weather_data()
    
    if not data:
        print("[ERROR] Failed to fetch weather data. Exiting.")
        return False
    
    print("\n[2/3] Parsing weather data...")
    records = fetch_weather.parse_weather_data(data)
    
    if not records:
        print("[ERROR] No weather records parsed. Exiting.")
        return False
    
    # Step 3: Store data in database
    print("\n[3/3] Storing data in database...")
    success_count = database.insert_weather_records(records)
    
    if success_count > 0:
        print(f"\n{'='*60}")
        print(f"[OK] Pipeline completed successfully!")
        print(f"  - Records fetched: {len(records)}")
        print(f"  - Records stored: {success_count}")
        print(f"{'='*60}")
        
        # Display statistics
        print("\nDatabase Statistics:")
        stats = database.get_database_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        return True
    else:
        print("\n[ERROR] Failed to store records in database")
        return False


if __name__ == "__main__":
    main()
