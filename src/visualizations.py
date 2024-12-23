from data_processing import specific_manufacturers_filtered
import os
import pandas as pd
import matplotlib.pyplot as plt

# Convert Real-World CO2 and Real-World MPG columns to numeric, coercing errors to NaN
specific_manufacturers_filtered['Real-World CO2 (g/mi)'] = pd.to_numeric(
    specific_manufacturers_filtered['Real-World CO2 (g/mi)'], errors='coerce'
)
specific_manufacturers_filtered['Real-World MPG'] = pd.to_numeric(
    specific_manufacturers_filtered['Real-World MPG'], errors='coerce'
)

# Interpolate missing values (NaN) in Real-World CO2 and Real-World MPG columns
specific_manufacturers_filtered['Real-World CO2 (g/mi)'] = specific_manufacturers_filtered['Real-World CO2 (g/mi)'].interpolate(method='linear')
specific_manufacturers_filtered['Real-World MPG'] = specific_manufacturers_filtered['Real-World MPG'].interpolate(method='linear')

# Remove invalid rows (negative or zero values)
specific_manufacturers_filtered = specific_manufacturers_filtered[
    (specific_manufacturers_filtered['Real-World CO2 (g/mi)'] > 0) &
    (specific_manufacturers_filtered['Real-World MPG'] > 0)
]

# Directory to save the plots
plots_dir = "manufacturer_co2_mpg_plots"
os.makedirs(plots_dir, exist_ok=True)

# Iterate through each manufacturer and generate the plots
for manufacturer in specific_manufacturers_filtered['Manufacturer'].unique():
    # Filter data for the manufacturer
    manufacturer_data = specific_manufacturers_filtered[
        specific_manufacturers_filtered['Manufacturer'] == manufacturer
    ]

    # Ensure data is sorted by Model Year
    manufacturer_data = manufacturer_data.sort_values(by='Model Year')

    # Aggregate both Real-World CO2 and Real-World MPG
    manufacturer_data = manufacturer_data.groupby('Model Year', as_index=False).agg({
        'Real-World CO2 (g/mi)': 'mean',
        'Real-World MPG': 'mean'
    })

    # Plot 1: Real-World CO2 (g/mi) over time
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
    ax.set_facecolor('black')
    ax.plot(
        manufacturer_data['Model Year'],
        manufacturer_data['Real-World CO2 (g/mi)'],
        marker='o',
        linestyle='-',
        linewidth=2,
        color='cyan',
        label='Real-World CO2 (g/mi)'
    )
    ax.set_xlabel("Year", fontsize=14, weight='bold', color='white')
    ax.set_ylabel("CO2 Emissions (g/mi)", fontsize=14, weight='bold', color='white')
    ax.tick_params(axis='x', colors='white', labelsize=12)
    ax.tick_params(axis='y', colors='white', labelsize=12)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.legend(loc='upper left', fontsize=12, facecolor='black', edgecolor='white', labelcolor='white')
    ax.set_title(f"{manufacturer} CO2 Emissions Over Time", fontsize=16, weight='bold', color='white')
    fig.savefig(f"{plots_dir}/{manufacturer}_co2_plot.png", dpi=300, facecolor='black')
    plt.close(fig)

    # Plot 2: Real-World MPG over time
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
    ax.set_facecolor('black')
    ax.plot(
        manufacturer_data['Model Year'],
        manufacturer_data['Real-World MPG'],
        marker='o',
        linestyle='-',
        linewidth=2,
        color='lime',
        label='Real-World MPG'
    )
    ax.set_xlabel("Year", fontsize=14, weight='bold', color='white')
    ax.set_ylabel("Fuel Efficiency (MPG)", fontsize=14, weight='bold', color='white')
    ax.tick_params(axis='x', colors='white', labelsize=12)
    ax.tick_params(axis='y', colors='white', labelsize=12)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.legend(loc='upper left', fontsize=12, facecolor='black', edgecolor='white', labelcolor='white')
    ax.set_title(f"{manufacturer} MPG Over Time", fontsize=16, weight='bold', color='white')
    fig.savefig(f"{plots_dir}/{manufacturer}_mpg_plot.png", dpi=300, facecolor='black')
    plt.close(fig)

    print(f"Enhanced dark-mode plots for {manufacturer} saved successfully!")


# Other visualizations and metrics for the homepage, where we discuss the importance of environmental impact and describe our exploration and how we are defining it