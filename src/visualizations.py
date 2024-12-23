from data_processing import specific_manufacturers_filtered
import os
import pandas as pd
import matplotlib.pyplot as plt


'''Real-World CO2 (g/mi) and Ton-MPG (Real-World) plots for each individual manufacturer. As these are the most important metrics determining environmental impact'''

# Convert Real-World CO2 and Real-World MPG columns to numeric, coercing errors to NaN
specific_manufacturers_filtered['Real-World CO2 (g/mi)'] = pd.to_numeric(
    specific_manufacturers_filtered['Real-World CO2 (g/mi)'], errors='coerce'
)
specific_manufacturers_filtered['Real-World MPG'] = pd.to_numeric(
    specific_manufacturers_filtered['Real-World MPG'], errors='coerce'
)

# Interpolate missing values (NaN) in Real-World CO2 and Ton-MPG columns
specific_manufacturers_filtered['Real-World CO2 (g/mi)'] = specific_manufacturers_filtered['Real-World CO2 (g/mi)'].interpolate(method='linear')
specific_manufacturers_filtered['Real-World MPG'] = specific_manufacturers_filtered['Real-World MPG'].interpolate(method='linear')


# Remove invalid rows (negative or zero values)
specific_manufacturers_filtered = specific_manufacturers_filtered[
    (specific_manufacturers_filtered['Real-World CO2 (g/mi)'] > 0) &
    (specific_manufacturers_filtered['Real-World MPG'] > 0)
]

# Check whether its cleaned and in the correct numeric format for further plotting and visualizations
print(specific_manufacturers_filtered[['Manufacturer', 'Model Year', 'Real-World CO2 (g/mi)', 'Real-World MPG']].head())
print(specific_manufacturers_filtered[['Model Year','Real-World CO2 (g/mi)', 'Real-World MPG']].dtypes)

# Directory to save the plots
plots_dir = "manufacturer_co2_mpg_plots"
os.makedirs(plots_dir, exist_ok=True)  # Create the directory if it doesn't exist

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
    plt.figure(figsize=(8, 6), facecolor='black')  # Black background for the figure
    ax = plt.gca()  # Get the current axis
    ax.set_facecolor('black')  # Set axes background to black
    plt.plot(
        manufacturer_data['Model Year'],
        manufacturer_data['Real-World CO2 (g/mi)'],
        marker='o',
        linestyle='-',
        linewidth=2,
        color='cyan'  # Cyan line color for visibility
    )
    plt.xlabel("Year", fontsize=12, weight='bold', color='white')  # White labels
    plt.ylabel("Real-World CO2 (g/mi)", fontsize=12, weight='bold', color='white')
    plt.xticks(fontsize=10, color='white')  # White tick labels
    plt.yticks(fontsize=10, color='white')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)  # Subtle gray gridlines
    plt.tight_layout()
    plt.savefig(f"{plots_dir}/{manufacturer}_co2_plot.png", dpi=300, facecolor='black')  # Save with black background
    plt.close()

    # Plot 2: Real-World MPG over time
    plt.figure(figsize=(8, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.plot(
        manufacturer_data['Model Year'],
        manufacturer_data['Real-World MPG'],
        marker='o',
        linestyle='-',
        linewidth=2,
        color='lime'  # Lime line color for contrast
    )
    plt.xlabel("Year", fontsize=12, weight='bold', color='white')
    plt.ylabel("Real-World MPG", fontsize=12, weight='bold', color='white')
    plt.xticks(fontsize=10, color='white')
    plt.yticks(fontsize=10, color='white')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{plots_dir}/{manufacturer}_mpg_plot.png", dpi=300, facecolor='black')
    plt.close()

    print(f"Enhanced dark-mode plots for {manufacturer} saved successfully!")



# Other visualizations and metrics for the homepage, where we discuss the importance of environmental impact and describe our exploration and how we are defining it