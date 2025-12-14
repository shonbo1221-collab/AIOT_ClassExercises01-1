"""
Create Test Data
Generates sample weather data for testing the application
"""

import database
from datetime import datetime


def create_test_data():
    """
    Create sample weather data for testing
    """
    print("Creating test weather data...")
    
    # Initialize database
    database.init_database()
    
    # Sample weather data for Taiwan locations
    test_records = [
        # 北部
        {'location': '臺北市', 'region': '北部', 'min_temp': 18.5, 'max_temp': 25.3, 'current_temp': 22.0, 'description': '多雲時晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '新北市', 'region': '北部', 'min_temp': 17.8, 'max_temp': 24.5, 'current_temp': 21.2, 'description': '晴時多雲', 'forecast_time': datetime.now().isoformat()},
        {'location': '基隆市', 'region': '北部', 'min_temp': 19.2, 'max_temp': 23.8, 'current_temp': 21.5, 'description': '多雲短暫雨', 'forecast_time': datetime.now().isoformat()},
        {'location': '桃園市', 'region': '北部', 'min_temp': 18.0, 'max_temp': 26.0, 'current_temp': 22.5, 'description': '晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '新竹縣', 'region': '北部', 'min_temp': 17.5, 'max_temp': 25.5, 'current_temp': 21.8, 'description': '多雲', 'forecast_time': datetime.now().isoformat()},
        {'location': '宜蘭縣', 'region': '北部', 'min_temp': 20.0, 'max_temp': 24.0, 'current_temp': 22.2, 'description': '陰短暫雨', 'forecast_time': datetime.now().isoformat()},
        
        # 中部
        {'location': '苗栗縣', 'region': '中部', 'min_temp': 16.5, 'max_temp': 27.0, 'current_temp': 22.0, 'description': '晴時多雲', 'forecast_time': datetime.now().isoformat()},
        {'location': '臺中市', 'region': '中部', 'min_temp': 19.0, 'max_temp': 28.5, 'current_temp': 24.0, 'description': '晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '彰化縣', 'region': '中部', 'min_temp': 20.0, 'max_temp': 29.0, 'current_temp': 25.0, 'description': '多雲時晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '南投縣', 'region': '中部', 'min_temp': 15.0, 'max_temp': 26.5, 'current_temp': 21.0, 'description': '晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '雲林縣', 'region': '中部', 'min_temp': 20.5, 'max_temp': 30.0, 'current_temp': 26.0, 'description': '晴時多雲', 'forecast_time': datetime.now().isoformat()},
        
        # 南部
        {'location': '嘉義縣', 'region': '南部', 'min_temp': 21.0, 'max_temp': 30.5, 'current_temp': 26.5, 'description': '晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '臺南市', 'region': '南部', 'min_temp': 22.0, 'max_temp': 31.0, 'current_temp': 27.0, 'description': '晴時多雲', 'forecast_time': datetime.now().isoformat()},
        {'location': '高雄市', 'region': '南部', 'min_temp': 23.0, 'max_temp': 32.0, 'current_temp': 28.0, 'description': '晴', 'forecast_time': datetime.now().isoformat()},
        {'location': '屏東縣', 'region': '南部', 'min_temp': 23.5, 'max_temp': 32.5, 'current_temp': 28.5, 'description': '晴時多雲', 'forecast_time': datetime.now().isoformat()},
        
        # 東部
        {'location': '花蓮縣', 'region': '東部', 'min_temp': 20.5, 'max_temp': 27.0, 'current_temp': 24.0, 'description': '多雲短暫雨', 'forecast_time': datetime.now().isoformat()},
        {'location': '臺東縣', 'region': '東部', 'min_temp': 22.0, 'max_temp': 29.0, 'current_temp': 26.0, 'description': '多雲時晴', 'forecast_time': datetime.now().isoformat()},
        
        # 離島
        {'location': '澎湖縣', 'region': '離島', 'min_temp': 21.5, 'max_temp': 26.5, 'current_temp': 24.5, 'description': '多雲', 'forecast_time': datetime.now().isoformat()},
        {'location': '金門縣', 'region': '離島', 'min_temp': 19.0, 'max_temp': 25.0, 'current_temp': 22.5, 'description': '晴時多雲', 'forecast_time': datetime.now().isoformat()},
        {'location': '連江縣', 'region': '離島', 'min_temp': 18.0, 'max_temp': 23.0, 'current_temp': 21.0, 'description': '多雲', 'forecast_time': datetime.now().isoformat()},
    ]
    
    # Insert test data
    success_count = database.insert_weather_records(test_records)
    
    print(f"\n[OK] Created {success_count} test weather records")
    
    # Display statistics
    stats = database.get_database_stats()
    print("\nDatabase Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return success_count > 0


if __name__ == "__main__":
    create_test_data()
