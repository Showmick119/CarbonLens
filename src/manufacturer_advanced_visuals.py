import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.patches import Patch
import numpy as np
from random_forest_model import aggregated_scores
from data_processing import specific_manufacturers_filtered

# Exclude Tesla from the dataset
aggregated_scores = aggregated_scores[aggregated_scores['Manufacturer'] != 'Tesla']

# Directory to save advanced visuals
plots_dir = "manufacturer_advanced_visuals"
os.makedirs(plots_dir, exist_ok=True)

# 1. **CO2 Reduction Rate Over Time (Bar Graph)**
for manufacturer in aggregated_scores['Manufacturer'].unique():
    data = aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer]
    data = data.sort_values(by='Model Year')
    data['CO2 Reduction Rate (%)'] = data['Yearly Sustainability Score'].pct_change() * 100

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(
        data['Model Year'],
        data['CO2 Reduction Rate (%)'],
        color='cyan',
        edgecolor='white'
    )
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_facecolor('none')  # Transparent background
    fig.patch.set_alpha(0)
    ax.set_xlabel("Year", fontsize=12, color='white')
    ax.set_ylabel("CO2 Reduction Rate (%)", fontsize=12, color='white')
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)

    # Add y-axis gridlines
    ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)  # Transparent gridlines

    plt.tight_layout()
    fig.savefig(f"{plots_dir}/{manufacturer}_co2_reduction_rate.png", dpi=300, transparent=True, bbox_inches='tight')
    plt.close(fig)

# 2. **MPG Efficiency Growth Rate (Bar Graph)**
for manufacturer in aggregated_scores['Manufacturer'].unique():
    data = aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer]
    data = data.sort_values(by='Model Year')
    data['MPG Growth Rate (%)'] = data['Yearly Sustainability Score'].pct_change() * 100

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(
        data['Model Year'],
        data['MPG Growth Rate (%)'],
        color='#228B22',  # Forest green
        edgecolor='white'
    )
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_facecolor('none')  # Transparent background
    fig.patch.set_alpha(0)
    ax.set_xlabel("Year", fontsize=12, color='white')
    ax.set_ylabel("MPG Growth Rate (%)", fontsize=12, color='white')
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)
    
    # Add y-axis gridlines
    ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)  # Transparent gridlines

    plt.tight_layout()
    fig.savefig(f"{plots_dir}/{manufacturer}_mpg_growth_rate.png", dpi=300, transparent=True, bbox_inches='tight')
    plt.close(fig)

# 3. **Sustainability Growth Over Time (Line Graph for Each Manufacturer)**
# Generate a colormap to assign a distinct color to each manufacturer
unique_manufacturers = aggregated_scores['Manufacturer'].unique()
cmap = plt.get_cmap('tab20', len(unique_manufacturers))  # Use updated get_cmap
color_map = {manufacturer: cmap(i) for i, manufacturer in enumerate(unique_manufacturers)}

fig, ax = plt.subplots(figsize=(12, 6))  # Wide layout

for manufacturer in unique_manufacturers:
    data = aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer]
    data = data.sort_values(by='Model Year')
    
    ax.plot(
        data['Model Year'],
        data['Yearly Sustainability Score'],
        marker='o',
        color=color_map[manufacturer],  # Assign a distinct color from the colormap
        label=manufacturer  # Add manufacturer to legend
    )

# Graph aesthetic adjustments
ax.set_facecolor('none')  # Transparent background
fig.patch.set_alpha(0)
ax.set_xlabel("Year", fontsize=12, color='white')  # No bold axis titles
ax.set_ylabel("Sustainability Score", fontsize=12, color='white')  # Axis title exists
ax.tick_params(axis='x', colors='white', labelsize=10)
ax.tick_params(axis='y', colors='white', labelsize=10)

# Adding a nice rounded legend with white font
legend = ax.legend(
    loc="upper left",
    fontsize=10,
    frameon=True,
    facecolor='none',  # Transparent background for the legend
    edgecolor='white'
)

# Adjust font color in legend manually
for text in legend.get_texts():
    text.set_color('white')

legend.get_frame().set_linewidth(0.8)

# Save the plot
plt.tight_layout()
fig.savefig(f"{plots_dir}/all_manufacturers_sustainability_growth_updated.png", dpi=300, transparent=True, bbox_inches='tight')
plt.close(fig)

# 4. **Comparative Boxplot for Sustainability Scores**
fig, ax = plt.subplots(figsize=(10, 6))  # Adjusted dimensions
aggregated_scores.boxplot(
    by='Manufacturer',
    column=['Yearly Sustainability Score'],
    grid=False,
    patch_artist=True,
    boxprops=dict(facecolor='#6B8E23', color='white'),  # Updated face color
    medianprops=dict(color='white'),
    whiskerprops=dict(color='white'),
    capprops=dict(color='white'),
    flierprops=dict(marker='o', markerfacecolor='#6B8E23', markeredgecolor='white', markersize=6),  # Ensure flier visibility
    ax=ax
)
ax.set_facecolor('none')  # Transparent background
fig.patch.set_alpha(0)

# Add x-axis and y-axis titles with white color
ax.set_xlabel("Manufacturer", fontsize=12, color='white')  # Explicitly set x-axis title
ax.set_ylabel("Yearly Sustainability Score", fontsize=12, color='white')  # Add y-axis title

# Customize tick parameters
ax.tick_params(axis='x', colors='white', labelsize=10, rotation=45)
ax.tick_params(axis='y', colors='white', labelsize=10)

# Remove default Matplotlib titles
ax.set_title("")
plt.suptitle("")

plt.tight_layout()
fig.savefig(f"{plots_dir}/comparative_sustainability_boxplot.png", dpi=300, transparent=True, bbox_inches='tight')
plt.close(fig)

# 5. **Powertrain Pie Chart for Each Manufacturer**
# Replace Manufacturer names in the specific_manufacturers_filtered DataFrame to their full-form names
specific_manufacturers_filtered['Manufacturer'] = specific_manufacturers_filtered['Manufacturer'].replace({
    'VW': 'Volkswagen',
    'GM': 'General Motors'
})

# Clean the powertrain columns
powertrain_columns = [
    'Powertrain - Diesel', 
    'Powertrain - Battery Electric Vehicle (BEV)',
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)',
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)',
    'Powertrain - Other (incl. CNG)',
    'Powertrain - Gasoline Mild Hybrid/MHEV',
    'Powertrain - Gasoline Strong Hybrid/HEV',
    'Powertrain - Gasoline with Start/Stop',
    'Powertrain - Gasoline without Start/Stop'
]

for powertrain in powertrain_columns:
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].replace('-', 0)
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].astype(str)
    
    # Detect if value is a percentage and convert to decimal
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].apply(
        lambda x: float(x.strip('%')) / 100 if '%' in x else float(x)
    )

# Define colors for powertrain categories
powertrain_colors = {
    'Powertrain - Diesel': '#ff9999',
    'Powertrain - Battery Electric Vehicle (BEV)': '#66b3ff',
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)': '#99ff99',
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)': '#ffcc99',
    'Powertrain - Other (incl. CNG)': '#c2c2f0',
    'Powertrain - Gasoline Mild Hybrid/MHEV': '#ffb3e6',
    'Powertrain - Gasoline Strong Hybrid/HEV': '#c2f0c2',
    'Powertrain - Gasoline with Start/Stop': '#ff6666',
    'Powertrain - Gasoline without Start/Stop': '#c2c2c2',
}

# Filter for 2024 data
specific_2024 = specific_manufacturers_filtered[specific_manufacturers_filtered['Model Year'] == 2024]

for manufacturer in specific_2024['Manufacturer'].unique():
    # Filter rows for the specific manufacturer
    manufacturer_data = specific_2024[specific_2024['Manufacturer'] == manufacturer]

    # Aggregate the powertrain columns by summing
    powertrain_distribution = manufacturer_data[powertrain_columns].sum()

    # Normalize the distribution to ensure it sums to 1
    powertrain_distribution = powertrain_distribution / powertrain_distribution.sum()

    # Generate labels for the legend including percentages
    legend_labels = [
        f"{category} - {percentage:.1%}"
        for category, percentage in zip(powertrain_distribution.index, powertrain_distribution.values)
    ]

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(12, 4))  # Adjusted size for aesthetics
    wedges, texts = ax.pie(
        powertrain_distribution,
        colors=[powertrain_colors[col] for col in powertrain_distribution.index],
        startangle=90,  # Starts at the top
        wedgeprops=dict(width=1.0)  # Full-filled pie
    )

    # Add legend on the left side of the chart with percentage values
    legend_elements = [
        Patch(facecolor=powertrain_colors[col], label=label)
        for col, label in zip(powertrain_distribution.index, legend_labels)
    ]
    ax.legend(
        handles=legend_elements,
        loc='center right',
        bbox_to_anchor=(0.0, 0.5),  # Reduced spacing between pie and legend
        frameon=False,
        fontsize=9,  # Reduced font size by ~15%
        labelcolor='white',
    )

    # Remove the title
    fig.patch.set_alpha(0)  # Transparent background
    ax.set_facecolor('none')  # Transparent face color

    # Save the pie chart
    plt.tight_layout()
    fig.savefig(
        f"{plots_dir}/{manufacturer}_powertrain_pie_chart.png",
        dpi=300,
        transparent=True,
        bbox_inches='tight',
    )
    plt.close(fig)

print("All advanced visuals have been successfully created.")