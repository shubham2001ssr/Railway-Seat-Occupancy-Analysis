import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

import os

# Configuration
NUM_TRAINS = 5
START_DATE = datetime(2023, 10, 1)
END_DATE = datetime(2023, 12, 31)  # 3 months of data
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/railway_booking_data.csv")

# Coach Configuration
COACH_CONFIG = {
    'Sleeper': {'prefix': 'S', 'count': 8, 'seats': 72},
    'AC 3 Tier': {'prefix': 'B', 'count': 4, 'seats': 64},
    'AC 2 Tier': {'prefix': 'A', 'count': 2, 'seats': 48},
    'Chair Car': {'prefix': 'C', 'count': 2, 'seats': 70}
}

# Quota Distribution (Approximate probabilities)
QUOTAS = ['General', 'Tatkal', 'Ladies', 'Senior Citizen']
QUOTA_PROBS = [0.70, 0.15, 0.10, 0.05]

def generate_dates(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

def generate_data():
    data = []
    
    dates = list(generate_dates(START_DATE, END_DATE))
    
    print(f"Generating data for {len(dates)} days and {NUM_TRAINS} trains...")
    
    for date in dates:
        # Weekend factor (higher occupancy on weekends)
        is_weekend = date.weekday() >= 5
        base_occupancy = 0.70 if is_weekend else 0.50
        
        # Festival factor (Diwali/Christmas approx)
        is_festival = (date.month == 11 and 10 <= date.day <= 15) or (date.month == 12 and 20 <= date.day <= 31)
        if is_festival:
            base_occupancy += 0.20
            
        base_occupancy = min(base_occupancy, 0.95)

        for train_id in range(101, 101 + NUM_TRAINS):
            for class_name, config in COACH_CONFIG.items():
                for coach_num in range(1, config['count'] + 1):
                    coach_code = f"{config['prefix']}{coach_num}"
                    
                    for seat_no in range(1, config['seats'] + 1):
                        # Determine if booked
                        # Random variation
                        booking_prob = base_occupancy + random.uniform(-0.1, 0.1)
                        # Popular classes might be higher
                        if class_name == 'Sleeper':
                            booking_prob += 0.1
                        
                        booking_prob = min(max(booking_prob, 0.0), 1.0)
                        
                        status = 'Booked' if random.random() < booking_prob else 'Available'
                        
                        quota = 'General'
                        if status == 'Booked':
                            quota = np.random.choice(QUOTAS, p=QUOTA_PROBS)
                        
                        entry = {
                            'Train_ID': train_id,
                            'Date': date.strftime('%Y-%m-%d'),
                            'Coach': coach_code,
                            'Seat_No': seat_no,
                            'Class': class_name,
                            'Quota': quota,
                            'Status': status
                        }
                        data.append(entry)

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_data()
    print(f"Generated {len(df)} records.")
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data saved to {OUTPUT_FILE}")
