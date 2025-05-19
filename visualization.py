"""Visualization utilities"""
import seaborn as sns
import matplotlib.pyplot as plt
import folium


def plot_delivery_times(data, x, title, filename):
    """Create delivery performance plot"""
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=x, y='delivery_time_hours')
    plt.title(title)
    plt.xlabel('')
    plt.ylabel('Delivery Time (hours)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def create_heatmap(data, index, columns, values, title, filename):
    """Generate performance heatmap"""
    pivot = data.pivot_table(index=index, columns=columns, values=values, aggfunc='mean')

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=.5)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def generate_interactive_map(data, lat_col, lon_col, size_col, color_col, filename):
    """Create Folium interactive map"""
    map_center = [data[lat_col].mean(), data[lon_col].mean()]
    m = folium.Map(location=map_center, zoom_start=4, tiles='OpenStreetMap')

    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=row[size_col] / 3,
            popup=f"Region: {row['destination_region']}<br>Service: {row['service_type']}<br>Delivery Time: {row[color_col]:.1f} hours",
            color='#3186cc',
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    m.save(filename)