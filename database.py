"""
Database Module
Handles SQLite database operations for weather data storage
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import os


DB_NAME = "data.db"


def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        sqlite3.Connection object
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_database():
    """
    Initialize the database and create tables if they don't exist
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create weather table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            region TEXT,
            min_temp REAL,
            max_temp REAL,
            current_temp REAL,
            description TEXT,
            forecast_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"[OK] Database initialized: {DB_NAME}")


def insert_weather_record(record: Dict) -> bool:
    """
    Insert a single weather record into the database
    
    Args:
        record: Dictionary containing weather data
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO weather (location, region, min_temp, max_temp, current_temp, description, forecast_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.get('location'),
            record.get('region'),
            record.get('min_temp'),
            record.get('max_temp'),
            record.get('current_temp'),
            record.get('description'),
            record.get('forecast_time')
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return False


def insert_weather_records(records: List[Dict]) -> int:
    """
    Insert multiple weather records into the database
    
    Args:
        records: List of weather record dictionaries
        
    Returns:
        Number of records successfully inserted
    """
    success_count = 0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for record in records:
        try:
            cursor.execute('''
                INSERT INTO weather (location, region, min_temp, max_temp, current_temp, description, forecast_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                record.get('location'),
                record.get('region'),
                record.get('min_temp'),
                record.get('max_temp'),
                record.get('current_temp'),
                record.get('description'),
                record.get('forecast_time')
            ))
            success_count += 1
        except sqlite3.Error as e:
            print(f"[ERROR] Error inserting record for {record.get('location')}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"[OK] Inserted {success_count}/{len(records)} records into database")
    return success_count


def get_all_weather_records() -> List[Dict]:
    """
    Retrieve all weather records from the database
    
    Returns:
        List of weather records as dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, location, region, min_temp, max_temp, current_temp, description, forecast_time, created_at
        FROM weather
        ORDER BY created_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'location': row['location'],
            'region': row['region'],
            'min_temp': row['min_temp'],
            'max_temp': row['max_temp'],
            'current_temp': row['current_temp'],
            'description': row['description'],
            'forecast_time': row['forecast_time'],
            'created_at': row['created_at']
        })
    
    return records


def get_latest_weather_records() -> List[Dict]:
    """
    Retrieve the most recent weather records (one per location)
    
    Returns:
        List of latest weather records as dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT w1.*
        FROM weather w1
        INNER JOIN (
            SELECT location, MAX(created_at) as max_created
            FROM weather
            GROUP BY location
        ) w2 ON w1.location = w2.location AND w1.created_at = w2.max_created
        ORDER BY w1.region, w1.location
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'location': row['location'],
            'region': row['region'],
            'min_temp': row['min_temp'],
            'max_temp': row['max_temp'],
            'current_temp': row['current_temp'],
            'description': row['description'],
            'forecast_time': row['forecast_time'],
            'created_at': row['created_at']
        })
    
    return records


def clear_old_records(days: int = 7):
    """
    Delete weather records older than specified days
    
    Args:
        days: Number of days to keep (default: 7)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM weather
        WHERE created_at < datetime('now', '-' || ? || ' days')
    ''', (days,))
    
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"[OK] Deleted {deleted_count} old records (older than {days} days)")


def get_database_stats() -> Dict:
    """
    Get database statistics
    
    Returns:
        Dictionary with database statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total records
    cursor.execute('SELECT COUNT(*) as count FROM weather')
    total_records = cursor.fetchone()['count']
    
    # Unique locations
    cursor.execute('SELECT COUNT(DISTINCT location) as count FROM weather')
    unique_locations = cursor.fetchone()['count']
    
    # Latest update time
    cursor.execute('SELECT MAX(created_at) as latest FROM weather')
    latest_update = cursor.fetchone()['latest']
    
    # Temperature range
    cursor.execute('SELECT MIN(min_temp) as min, MAX(max_temp) as max FROM weather WHERE min_temp IS NOT NULL AND max_temp IS NOT NULL')
    temp_row = cursor.fetchone()
    min_temp = temp_row['min']
    max_temp = temp_row['max']
    
    conn.close()
    
    return {
        'total_records': total_records,
        'unique_locations': unique_locations,
        'latest_update': latest_update,
        'min_temp': min_temp,
        'max_temp': max_temp
    }


def main():
    """
    Main function to test database operations
    """
    print("=" * 60)
    print("Database Module Test")
    print("=" * 60)
    
    # Initialize database
    init_database()
    
    # Test insert
    test_record = {
        'location': '臺北市',
        'region': '北部',
        'min_temp': 18.5,
        'max_temp': 25.3,
        'current_temp': 22.0,
        'description': '多雲時晴',
        'forecast_time': datetime.now().isoformat()
    }
    
    print("\nInserting test record...")
    insert_weather_record(test_record)
    
    # Get stats
    print("\nDatabase Statistics:")
    stats = get_database_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Get records
    print("\nRetrieving records...")
    records = get_latest_weather_records()
    print(f"Found {len(records)} records")
    
    if records:
        print("\nSample record:")
        record = records[0]
        for key, value in record.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
