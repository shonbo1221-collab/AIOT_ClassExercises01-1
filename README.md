# 台灣天氣資料管道系統

AIoT 課程專案 - 從中央氣象署 API 下載天氣資料，儲存至 SQLite 資料庫，並透過 Streamlit 視覺化呈現。

## 🌐 線上 Demo

**[🚀 立即體驗線上版本](https://aiotclassexercises01-1-lyasebxd2uy5pgz57hbagd.streamlit.app/)**

> 線上版本部署於 Streamlit Cloud，可直接查看台灣溫度分布地圖與即時天氣資料。

## 📋 專案目標

1. ✅ 下載中央氣象署 JSON 資料
2. ✅ 解析資料並取出各地區的溫度資訊
3. ✅ 設計 SQLite 資料庫儲存資料
4. ✅ 將解析後的資料存入 SQLite3
5. ✅ 建立 Streamlit App 顯示資料（模仿 CWA 溫度顯示介面）

## 🛠️ 技術架構

- **資料來源**: 中央氣象署開放資料平台 API
- **資料庫**: SQLite3 (`data.db`)
- **後端**: Python 3.x
- **前端**: Streamlit
- **視覺化**: Plotly

## 📦 專案結構

```
Hw1203/
├── fetch_weather.py    # 天氣資料下載與解析模組
├── database.py         # SQLite 資料庫操作模組
├── app.py             # Streamlit 網頁應用程式
├── main.py            # 主要管道執行腳本
├── requirements.txt   # Python 套件依賴
├── README.md          # 專案說明文件
└── data.db           # SQLite 資料庫（執行後自動建立）
```

## 🗄️ 資料庫結構

```sql
CREATE TABLE weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,           -- 地點名稱
    region TEXT,                       -- 地理區域（北部/中部/南部/東部/離島）
    min_temp REAL,                     -- 最低溫度
    max_temp REAL,                     -- 最高溫度
    current_temp REAL,                 -- 當前溫度
    description TEXT,                  -- 天氣描述
    forecast_time TEXT,                -- 預報時間
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 資料建立時間
);
```

## 🚀 安裝與執行

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 執行完整資料管道（下載 → 解析 → 儲存）

```bash
python main.py
```

這會執行以下步驟：
- 初始化資料庫
- 從 CWA API 下載天氣資料
- 解析 JSON 資料
- 將資料儲存到 SQLite 資料庫

### 3. 啟動 Streamlit 網頁應用程式

```bash
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`

## 🎨 Streamlit 介面功能

### 視覺化特色（模仿 CWA 溫度顯示）

- **🌡️ 色彩編碼溫度顯示**: 使用冷到熱的漸層色（藍色 → 綠色 → 黃色 → 橙色 → 紅色）
- **🗺️ 地理區域分組**: 依北部、中部、南部、東部、離島分類
- **📊 溫度分布圖**: 互動式長條圖顯示各地溫度
- **📋 資料表格**: 可排序、篩選的天氣資料表
- **🎨 溫度色階圖例**: 清楚標示溫度範圍對應的顏色

### 互動功能

- **🔄 更新天氣資料**: 即時從 API 下載最新資料
- **🗺️ 地區篩選**: 依地理區域篩選顯示資料
- **📊 統計資訊**: 顯示總記錄數、觀測站數、最高/最低溫
- **🗑️ 清除舊資料**: 刪除 7 天前的歷史資料

## 📊 溫度色階對照表

| 溫度範圍 | 顏色 | 描述 |
|---------|------|------|
| < 10°C | 深藍色 | 極冷 |
| 10-15°C | 藍色 | 冷 |
| 15-20°C | 淺藍色 | 涼 |
| 20-25°C | 淺綠色 | 舒適 |
| 25-28°C | 黃色 | 溫暖 |
| 28-32°C | 橙色 | 熱 |
| 32-35°C | 深橙色 | 很熱 |
| > 35°C | 紅色 | 極熱 |

## 🧪 測試個別模組

### 測試資料下載與解析

```bash
python fetch_weather.py
```

### 測試資料庫操作

```bash
python database.py
```

## 📝 API 資訊

- **API 端點**: `https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001`
- **資料格式**: JSON
- **更新頻率**: 依中央氣象署更新時間

## 🎓 課程要求檢核

- ✅ 下載中央氣象局 JSON 資料
- ✅ 解析資料取出各地區溫度
- ✅ 設計 SQLite 資料庫 (data.db)
- ✅ 使用 Python sqlite3 存入資料
- ✅ 建立 Streamlit App 顯示資料
- ✅ 附上螢幕截圖（執行後自動產生）

## 📸 螢幕截圖

執行 Streamlit 應用程式後，介面將顯示：
- 色彩編碼的溫度資料表
- 各地溫度分布圖
- 地區篩選功能
- 即時統計資訊

## 🔧 故障排除

### 資料庫檔案無法建立
- 確認目錄有寫入權限
- 檢查磁碟空間是否足夠

### API 請求失敗
- 檢查網路連線
- 確認 API 金鑰是否有效
- 查看 CWA 開放資料平台是否正常運作

### Streamlit 無法啟動
- 確認已安裝所有依賴套件
- 檢查 Python 版本 (建議 3.8+)
- 嘗試重新安裝 streamlit: `pip install --upgrade streamlit`

## 📄 授權

此專案為 AIoT 課程作業，僅供學習使用。

## 👨‍💻 作者

AIoT 課程學生專案
