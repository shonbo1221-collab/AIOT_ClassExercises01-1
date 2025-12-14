"""
Streamlit Weather Dashboard
Displays weather data from SQLite database with CWA-style interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import database
import fetch_weather
import main as pipeline


# Page configuration
st.set_page_config(
    page_title="台灣天氣資料儀表板",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Taiwan city coordinates (latitude, longitude)
CITY_COORDINATES = {
    # 北部
    '臺北': (25.0330, 121.5654),
    '臺北市': (25.0330, 121.5654),
    '新北': (25.0120, 121.4654),
    '新北市': (25.0120, 121.4654),
    '基隆': (25.1276, 121.7392),
    '基隆市': (25.1276, 121.7392),
    '桃園': (24.9936, 121.3010),
    '桃園市': (24.9936, 121.3010),
    '新竹': (24.8138, 120.9675),
    '新竹市': (24.8138, 120.9675),
    '新竹縣': (24.8387, 121.0177),
    '宜蘭': (24.7021, 121.7378),
    '宜蘭縣': (24.7021, 121.7378),
    
    # 中部
    '苗栗': (24.5602, 120.8214),
    '苗栗縣': (24.5602, 120.8214),
    '臺中': (24.1477, 120.6736),
    '臺中市': (24.1477, 120.6736),
    '彰化': (24.0518, 120.5161),
    '彰化縣': (24.0518, 120.5161),
    '南投': (23.9609, 120.9719),
    '南投縣': (23.9609, 120.9719),
    '雲林': (23.7092, 120.4313),
    '雲林縣': (23.7092, 120.4313),
    
    # 南部
    '嘉義': (23.4800, 120.4491),
    '嘉義市': (23.4800, 120.4491),
    '嘉義縣': (23.4518, 120.2554),
    '臺南': (22.9998, 120.2269),
    '臺南市': (22.9998, 120.2269),
    '高雄': (22.6273, 120.3014),
    '高雄市': (22.6273, 120.3014),
    '屏東': (22.6820, 120.4950),
    '屏東縣': (22.6820, 120.4950),
    
    # 東部
    '花蓮': (23.9871, 121.6015),
    '花蓮縣': (23.9871, 121.6015),
    '臺東': (22.7972, 121.0713),
    '臺東縣': (22.7972, 121.0713),
    
    # 離島
    '澎湖': (23.5711, 119.5793),
    '澎湖縣': (23.5711, 119.5793),
    '金門': (24.4491, 118.3765),
    '金門縣': (24.4491, 118.3765),
    '連江': (26.1605, 119.9512),
    '連江縣': (26.1605, 119.9512),
    '馬祖': (26.1605, 119.9512),
}


def get_temperature_color(temp: float) -> str:
    """
    Get color based on temperature value (cold to hot gradient)
    
    Args:
        temp: Temperature value
        
    Returns:
        Hex color code
    """
    if temp is None:
        return '#CCCCCC'
    
    # Temperature color scale (blue to red)
    if temp < 10:
        return '#0066CC'  # Dark blue (very cold)
    elif temp < 15:
        return '#3399FF'  # Blue (cold)
    elif temp < 20:
        return '#66CCFF'  # Light blue (cool)
    elif temp < 25:
        return '#99FF99'  # Light green (comfortable)
    elif temp < 28:
        return '#FFFF66'  # Yellow (warm)
    elif temp < 32:
        return '#FFCC33'  # Orange (hot)
    elif temp < 35:
        return '#FF6633'  # Dark orange (very hot)
    else:
        return '#CC0000'  # Red (extremely hot)


def style_temperature_cell(val):
    """
    Style temperature cells with background color
    """
    if pd.isna(val):
        return ''
    color = get_temperature_color(float(val))
    return f'background-color: {color}; color: white; font-weight: bold;'


def create_temperature_legend():
    """
    Create a temperature color legend
    """
    st.markdown("### 🌡️ 溫度色階")
    
    cols = st.columns(8)
    temp_ranges = [
        ("< 10°C", "#0066CC", "極冷"),
        ("10-15°C", "#3399FF", "冷"),
        ("15-20°C", "#66CCFF", "涼"),
        ("20-25°C", "#99FF99", "舒適"),
        ("25-28°C", "#FFFF66", "溫暖"),
        ("28-32°C", "#FFCC33", "熱"),
        ("32-35°C", "#FF6633", "很熱"),
        ("> 35°C", "#CC0000", "極熱"),
    ]
    
    for col, (range_text, color, label) in zip(cols, temp_ranges):
        with col:
            st.markdown(
                f"""
                <div style="background-color: {color}; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="color: white; font-weight: bold; font-size: 12px;">{label}</div>
                    <div style="color: white; font-size: 10px;">{range_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def display_statistics(stats: dict):
    """
    Display database statistics
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 總記錄數", stats['total_records'])
    
    with col2:
        st.metric("📍 觀測站數", stats['unique_locations'])
    
    with col3:
        if stats['min_temp'] is not None:
            st.metric("🥶 最低溫", f"{stats['min_temp']:.1f}°C")
        else:
            st.metric("🥶 最低溫", "N/A")
    
    with col4:
        if stats['max_temp'] is not None:
            st.metric("🥵 最高溫", f"{stats['max_temp']:.1f}°C")
        else:
            st.metric("🥵 最高溫", "N/A")


def display_weather_table(df: pd.DataFrame, region_filter: str = "全部"):
    """
    Display weather data table with color coding
    """
    # Filter by region
    if region_filter != "全部":
        df = df[df['地區'] == region_filter]
    
    if df.empty:
        st.warning("沒有資料可顯示")
        return
    
    # Create styled dataframe
    st.markdown("### 📋 天氣資料表")
    
    # Display table with color coding
    styled_df = df.style.applymap(
        style_temperature_cell,
        subset=['最低溫 (°C)', '最高溫 (°C)', '當前溫度 (°C)']
    )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=500
    )


def create_temperature_map(df: pd.DataFrame):
    """
    Create a temperature visualization map with Taiwan geography
    """
    if df.empty:
        return
    
    st.markdown("### 🗺️ 台灣溫度分布圖")
    
    # Prepare data for map
    map_data = []
    
    for _, row in df.iterrows():
        location = row['地點']
        
        # Get coordinates for this location
        coords = None
        # Try exact match first
        if location in CITY_COORDINATES:
            coords = CITY_COORDINATES[location]
        else:
            # Try partial match (remove 市/縣 suffix)
            for key in CITY_COORDINATES:
                if location.replace('市', '').replace('縣', '') in key or key in location:
                    coords = CITY_COORDINATES[key]
                    break
        
        if coords is None:
            continue
        
        # Get temperature
        temp = row['當前溫度 (°C)'] if pd.notna(row['當前溫度 (°C)']) else \
               (row['最低溫 (°C)'] + row['最高溫 (°C)']) / 2 if pd.notna(row['最低溫 (°C)']) and pd.notna(row['最高溫 (°C)']) else None
        
        if temp is not None:
            map_data.append({
                'location': location,
                'lat': coords[0],
                'lon': coords[1],
                'temp': temp,
                'region': row['地區'],
                'description': row['天氣描述'],
                'color': get_temperature_color(temp)
            })
    
    if not map_data:
        st.warning("無法顯示地圖：沒有找到對應的城市座標")
        return
    
    # Create map figure
    fig = go.Figure()
    
    # Add temperature markers
    for data in map_data:
        fig.add_trace(go.Scattergeo(
            lon=[data['lon']],
            lat=[data['lat']],
            text=f"{data['location']}<br>{data['temp']:.1f}°C",
            mode='markers+text',
            marker=dict(
                size=20,
                color=data['color'],
                line=dict(width=2, color='white')
            ),
            textfont=dict(
                size=10,
                color='black',
                family='Arial Black'
            ),
            textposition='top center',
            name=data['location'],
            showlegend=False,
            hovertemplate=f"<b>{data['location']}</b><br>" +
                         f"地區: {data['region']}<br>" +
                         f"溫度: {data['temp']:.1f}°C<br>" +
                         f"天氣: {data['description']}<extra></extra>"
        ))
    
    # Update map layout to focus on Taiwan
    fig.update_geos(
        center=dict(lon=120.9, lat=23.7),  # Center on Taiwan
        projection_scale=25,  # Zoom level
        visible=True,
        resolution=50,
        showcountries=True,
        countrycolor="lightgray",
        showcoastlines=True,
        coastlinecolor="gray",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        showocean=True,
        oceancolor="rgb(204, 229, 255)",
        showlakes=False,
        showrivers=False
    )
    
    fig.update_layout(
        title={
            'text': "台灣各地溫度分布",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=700,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main():
    """
    Main Streamlit application
    """
    # Header
    st.title("🌤️ 台灣天氣資料儀表板")
    st.markdown("**資料來源：中央氣象署 (CWA)**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ 控制面板")
        
        # Refresh button
        if st.button("🔄 更新天氣資料", use_container_width=True):
            with st.spinner("正在下載最新天氣資料..."):
                try:
                    pipeline.main()
                    st.success("✓ 資料更新成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"✗ 更新失敗: {e}")
        
        st.markdown("---")
        
        # Region filter
        st.subheader("🗺️ 地區篩選")
        region_filter = st.selectbox(
            "選擇地區",
            ["全部", "北部", "中部", "南部", "東部", "離島"]
        )
        
        st.markdown("---")
        
        # Database info
        st.subheader("ℹ️ 資料庫資訊")
        stats = database.get_database_stats()
        
        if stats['latest_update']:
            st.info(f"最後更新: {stats['latest_update']}")
        else:
            st.warning("尚無資料")
        
        st.markdown("---")
        
        # Clear old data button
        if st.button("🗑️ 清除舊資料 (7天前)", use_container_width=True):
            database.clear_old_records(7)
            st.success("✓ 舊資料已清除")
            st.rerun()
    
    # Main content
    # Initialize database
    database.init_database()
    
    # Get statistics
    stats = database.get_database_stats()
    
    # Display statistics
    display_statistics(stats)
    
    st.markdown("---")
    
    # Temperature legend
    create_temperature_legend()
    
    st.markdown("---")
    
    # Get weather data
    records = database.get_latest_weather_records()
    
    if not records:
        st.warning("⚠️ 資料庫中沒有天氣資料。請點擊側邊欄的「更新天氣資料」按鈕下載資料。")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Rename columns for display
    df_display = df.rename(columns={
        'location': '地點',
        'region': '地區',
        'min_temp': '最低溫 (°C)',
        'max_temp': '最高溫 (°C)',
        'current_temp': '當前溫度 (°C)',
        'description': '天氣描述',
        'forecast_time': '預報時間',
        'created_at': '資料時間'
    })
    
    # Select columns to display
    display_columns = ['地點', '地區', '最低溫 (°C)', '最高溫 (°C)', '當前溫度 (°C)', '天氣描述']
    df_display = df_display[display_columns]
    
    # Create temperature map
    create_temperature_map(df_display)
    
    st.markdown("---")
    
    # Display table
    display_weather_table(df_display, region_filter)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 12px;">
            <p>AIoT 課程專案 | 中央氣象署開放資料平台</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
