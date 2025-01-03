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

# Renaming GM and VW to their full form names
specific_manufacturers_filtered['Manufacturer'] = specific_manufacturers_filtered['Manufacturer'].replace({
    'GM': 'General Motors',
    'VW': 'Volkswagen'
})

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
    fig, ax = plt.subplots(figsize=(12, 5))  # Slightly larger aspect ratio
    ax.set_facecolor('none')  # Transparent axes background
    fig.patch.set_alpha(0)  # Transparent figure background
    ax.plot(
        manufacturer_data['Model Year'],
        manufacturer_data['Real-World CO2 (g/mi)'],
        marker='o',
        linestyle='-',
        linewidth=2,
        color='cyan',
        label='Real-World CO2 (g/mi)'
    )
    ax.set_xlabel("Year", fontsize=12, color='white')  # Non-bold labels
    ax.set_ylabel("CO2 Emissions (g/mi)", fontsize=12, color='white')  # Non-bold labels
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    # Updated legend with rounded box in the top-right corner
    legend = ax.legend(
        loc='upper right',
        fontsize=10,
        frameon=True,
        framealpha=0.5,
        facecolor='black',
        edgecolor='white',
        labelcolor='white'
    )
    legend.get_frame().set_linewidth(1.5)

    # Optimize space and save
    plt.tight_layout()  # Ensure graph fills the image
    fig.savefig(f"{plots_dir}/{manufacturer}_co2_plot.png", dpi=300, transparent=True, bbox_inches='tight')
    plt.close(fig)

    # Plot 2: Real-World MPG over time
    fig, ax = plt.subplots(figsize=(12, 5))  # Slightly larger aspect ratio
    ax.set_facecolor('none')  # Transparent axes background
    fig.patch.set_alpha(0)  # Transparent figure background
    ax.plot(
        manufacturer_data['Model Year'],
        manufacturer_data['Real-World MPG'],
        marker='o',
        linestyle='-',
        linewidth=2,
        color='#228B22',  # Forest green
        label='Real-World MPG'
    )
    ax.set_xlabel("Year", fontsize=12, color='white')  # Non-bold labels
    ax.set_ylabel("Fuel Efficiency (MPG)", fontsize=12, color='white')  # Non-bold labels
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    # Updated legend with rounded box in the top-left corner
    legend = ax.legend(
        loc='upper left',
        fontsize=10,
        frameon=True,
        framealpha=0.5,
        facecolor='black',
        edgecolor='white',
        labelcolor='white'
    )
    legend.get_frame().set_linewidth(1.5)

    # Optimize space and save
    plt.tight_layout()  # Ensure graph fills the image
    fig.savefig(f"{plots_dir}/{manufacturer}_mpg_plot.png", dpi=300, transparent=True, bbox_inches='tight')
    plt.close(fig)

    print(f"Updated transparent plots for {manufacturer} saved successfully!")