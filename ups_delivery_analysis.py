"""
IS 362 Final Project - UPS Delivery Performance Analysis
Main analysis script for PyCharm
"""
from data_utils import load_ups_data, scrape_weather_data
from visualization import plot_delivery_times, create_heatmap, generate_interactive_map
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import matplotlib.pyplot as plt
import os


class DeliveryAnalyzer:
    def __init__(self):
        self.df = None
        self.weather_df = None
        self.results = {}

    def execute(self):
        """Run full analysis pipeline"""
        print("Starting UPS Delivery Analysis")

        self._load_data()
        self._transform_data()
        self._analyze()
        self._visualize()
        self._advanced_analysis()

        print("\nAnalysis complete! Check /output folder for results")

    def _load_data(self):
        """Step 1: Data acquisition"""
        print("\n[1/5] Loading data...")
        self.df = load_ups_data('data/simulated_ups_data.csv')
        regions = self.df['destination_region'].unique()
        self.weather_df = scrape_weather_data(regions, '2023-01-01', '2023-03-31')

    def _transform_data(self):
        """Step 2: Data preparation"""
        print("\n[2/5] Transforming data...")
        self.df['shipment_date'] = pd.to_datetime(self.df['shipment_date'])
        self.df['delivery_date'] = pd.to_datetime(self.df['delivery_date'])

        self.df['delivery_time_hours'] = (
                (self.df['delivery_date'] - self.df['shipment_date']).dt.total_seconds() / 3600
        )
        self.df['time_of_day'] = pd.cut(
            self.df['delivery_hour'],
            bins=[0, 12, 17, 24],
            labels=['Morning', 'Afternoon', 'Evening']
        )

        self.df = pd.merge(
            self.df,
            self.weather_df,
            left_on=['delivery_date', 'destination_region'],
            right_on=['date', 'location']
        )

    def _analyze(self):
        """Step 3: Statistical analysis"""
        print("\n[3/5] Computing metrics...")
        self.results = {
            'avg_time': self.df['delivery_time_hours'].mean(),
            'on_time_rate': self.df['on_time'].mean() * 100,
            'time_of_day_impact': self.df.groupby('time_of_day')['delivery_time_hours'].mean(),
            'weather_impact': self.df.groupby('weather_condition')['on_time'].mean()
        }

        print("\nKey Metrics:")
        print(f"- Avg Delivery Time: {self.results['avg_time']:.1f} hours")
        print(f"- On-Time Rate: {self.results['on_time_rate']:.1f}%")

    def _visualize(self):
        """Step 4: Generate visualizations"""
        print("\n[4/5] Creating visualizations...")
        os.makedirs('output', exist_ok=True)

        plot_delivery_times(
            self.df,
            x='time_of_day',
            title='Delivery Performance by Time of Day',
            filename='output/time_of_day_impact.png'
        )

        create_heatmap(
            self.df,
            index='destination_region',
            columns='weather_condition',
            values='delivery_time_hours',
            title='Delivery Times by Region/Weather',
            filename='output/weather_heatmap.png'
        )

        generate_interactive_map(
            self.df,
            lat_col='latitude',
            lon_col='longitude',
            size_col='package_weight',
            color_col='delivery_time_hours',
            filename='output/delivery_map.html'
        )

    def _advanced_analysis(self):
        """Step 5: Time series decomposition"""
        print("\n[5/5] Running time series analysis...")
        ts_data = self.df.set_index('delivery_date').resample('D').size()
        decomposition = seasonal_decompose(ts_data, model='additive', period=7)

        plt.figure(figsize=(12, 8))
        decomposition.plot()
        plt.savefig('output/time_series_decomposition.png')
        plt.close()


if __name__ == "__main__":
    analyzer = DeliveryAnalyzer()
    analyzer.execute()