import pandas as pd
import numpy as np

try:
    print("Loading data...")
    df = pd.read_csv('../data/railway_booking_data.csv')
    print("Data loaded.")
    
    print("Calculating occupancy...")
    occupancy = df.groupby(['Train_ID', 'Date', 'Coach', 'Class'])['Status'].apply(lambda x: (x == 'Booked').mean()).reset_index(name='Occupancy_Rate')
    print("Occupancy calculated.")
    
    print("Generating heatmap data...")
    pivot_table = occupancy.pivot_table(index='Coach', columns='Date', values='Occupancy_Rate', aggfunc='mean')
    print("Heatmap data generated.")
    
    print("Analysis verification details:")
    print(f"Total records: {len(df)}")
    print(f"Average Occupancy: {occupancy['Occupancy_Rate'].mean():.2f}")
    
    print("Verification SUCCESS.")
except Exception as e:
    print(f"Verification FAILED: {e}")
    exit(1)
