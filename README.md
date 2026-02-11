# 🚄 Railway Seat Occupancy Heatmap Analysis (India)

![Dashboard Preview](dashboard_preview.png)

## 📌 Project Overview
This data analytics project analyzes **railway seat occupancy trends** in India using synthetic booking data. It is designed to provide insights into passenger demand, quota usage, and seasonal trends (festivals, weekends).

The project demonstrates a full-stack data analysis workflow:
1.  **Data Engineering**: Generating simulated booking data (~500k records) and loading it into a **SQLite Database**.
2.  **Data Analysis**: Using **Python (Pandas)** and **SQL** to extract key metrics.
3.  **Visualization**:
    - Interactive **Streamlit Dashboard** for real-time exploration.
    - Static **Seaborn/Matplotlib** heatmaps and charts for reporting.

## 📂 Directory Structure
```
├── data/                   # Generated CSV and SQLite database
├── dashboard/              # Streamlit Application
│   └── app.py
├── notebooks/              # Jupyter Notebooks
│   ├── analysis.ipynb      # Python-based analysis
│   └── sql_analysis.ipynb  # SQL-based analysis
├── scripts/                # Utility Scripts
│   ├── generate_data.py    # Data generation script
│   └── to_sql.py           # ETL script (CSV -> SQL)
├── requirements.txt        # Python dependencies
└── README.md               # Project Documentation
```

## 🛠️ Tech Stack
-   **Language**: Python 3.8+
-   **Libraries**: Pandas, NumPy, Seaborn, Matplotlib, Streamlit
-   **Database**: SQLite3
-   **Tools**: Jupyter Notebook, VS Code

## 🚀 Setup & How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Railway-Seat-Occupancy.git
cd Railway-Seat-Occupancy
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate the Database
**Important:** The `railway.db` file is not included in the repository to keep the download size small. You **must** generate it locally from the CSV file before running the dashboard.

```bash
python scripts/to_sql.py
```
*Note: This script reads `data/railway_booking_data.csv` and creates `data/railway.db`.*

### 5. Run the Dashboard
Launch the interactive dashboard to explore the data:
```bash
streamlit run dashboard/app.py
```

### 6. View Analysis (Optional)
Open `notebooks/analysis.ipynb` or `notebooks/sql_analysis.ipynb` in Jupyter Notebook to see the detailed code and static visualizations.

## 📊 Key Insights & Visualizations
-   **Seat Occupancy Heatmap**: Visualizes which coaches (e.g., S1 vs AC1) have the highest density.
-   **Quota Analysis**: Breakdown of bookings by General, Tatkal, Ladies, etc.
-   **Weekend Trends**: Bar charts confirming higher occupancy on weekends.