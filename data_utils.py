"""Data handling utilities"""
import pandas as pd
import numpy as np
import time


def load_ups_data(filepath):
    """Load UPS delivery data"""
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} UPS records")
        return df
    except FileNotFoundError:
        print("Warning: No data file found - generating sample data")
        return _generate_sample_data()


def scrape_weather_data(locations, start_date, end_date):
    """Simulate weather data collection"""
    print(f"Gathering weather data for {len(locations)} regions...")
    time.sleep(1)

    dates = pd.date_range(start_date, end_date)
    conditions = ['Clear', 'Rain', 'Snow', 'Fog']

    weather_data = []
    for loc in locations:
        data = {
            'location': loc,
            'date': dates,
            'temperature': np.random.randint(30, 90, len(dates)),
            'precipitation': np.round(np.random.random(len(dates)), 2),
            'weather_condition': np.random.choice(conditions, len(dates))
        }
        weather_data.append(pd.DataFrame(data))

    return pd.concat(weather_data)


def _generate_sample_data(records=500):
    """Generate simulated UPS data"""
    regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']
    services = ['Ground', '3-Day Select', '2nd Day Air', 'Next Day Air']

    return pd.DataFrame({
        'tracking_number': [f'1Z{np.random.randint(1000000, 9999999)}' for _ in range(records)],
        'shipment_date': pd.date_range('2023-01-01', periods=records, freq='H'),
        'delivery_date': pd.date_range('2023-01-02', periods=records, freq='H') + pd.to_timedelta(
            np.random.randint(1, 72, records), unit='H'),
        'delivery_hour': np.random.randint(8, 20, records),
        'package_weight': np.round(np.random.uniform(0.1, 50, records), 1),
        'destination_region': np.random.choice(regions, records),
        'service_type': np.random.choice(services, records),
        'latitude': np.random.uniform(35.0, 45.0, records),
        'longitude': np.random.uniform(-120.0, -70.0, records),
        'estimated_delivery_hours': np.random.choice([24, 36, 48, 72], records),
        'on_time': np.random.choice([True, False], records, p=[0.85, 0.15])
    })