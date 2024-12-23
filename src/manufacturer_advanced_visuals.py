import pandas as pd
import os
import matplotlib.pyplot as plt
from random_forest_model import aggregated_scores

# Exclude Tesla from the dataset
aggregated_scores = aggregated_scores[aggregated_scores['Manufacturer'] != 'Tesla']

# Directory to save advanced visuals
plots_dir = "manufacturer_advanced_visuals"
os.makedirs(plots_dir, exist_ok=True)

# Style configuration for modern visuals
plt.style.use('dark_background')

def configure_plot(xlabel, ylabel):
    """Helper function to apply consistent styling to plots."""
    plt.xlabel(xlabel, fontsize=14, color='white', labelpad=15)
    plt.ylabel(ylabel, fontsize=14, color='white', labelpad=15)
    plt.xticks(fontsize=12, color='white')
    plt.yticks(fontsize=12, color='white')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# 1. **CO2 Reduction Rate Over Time**
for manufacturer in aggregated_scores['Manufacturer'].unique():
    data = aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer]
    data = data.sort_values(by='Model Year')
    data['CO2 Reduction Rate (%)'] = data['Yearly Sustainability Score'].pct_change() * 100

    plt.figure(figsize=(12, 7), facecolor='black')
    plt.plot(data['Model Year'], data['CO2 Reduction Rate (%)'], marker='o', color='orange', linewidth=2)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.7)
    configure_plot("Year", "CO2 Reduction Rate (%)")
    plt.savefig(f"{plots_dir}/{manufacturer}_co2_reduction_rate.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()

# 2. **MPG Efficiency Growth Rate**
for manufacturer in aggregated_scores['Manufacturer'].unique():
    data = aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer]
    data = data.sort_values(by='Model Year')
    data['MPG Growth Rate (%)'] = data['Yearly Sustainability Score'].pct_change() * 100

    plt.figure(figsize=(12, 7), facecolor='black')
    plt.plot(data['Model Year'], data['MPG Growth Rate (%)'], marker='o', color='lime', linewidth=2)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.7)
    configure_plot("Year", "MPG Growth Rate (%)")
    plt.savefig(f"{plots_dir}/{manufacturer}_mpg_growth_rate.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()

# 3. **Top Manufacturers in Sustainability Efforts**
cumulative_improvement = aggregated_scores.groupby('Manufacturer')['Yearly Sustainability Score'].sum().sort_values()
plt.figure(figsize=(12, 7), facecolor='black')
cumulative_improvement.plot(kind='barh', color='cyan', edgecolor='black')
configure_plot("Cumulative Improvement", "Manufacturer")
plt.savefig(f"{plots_dir}/top_sustainability_efforts.png", dpi=300, facecolor='black', bbox_inches='tight')
plt.close()

# 4. **CO2-to-MPG Ratio Trends**
for manufacturer in aggregated_scores['Manufacturer'].unique():
    data = aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer]
    data = data.sort_values(by='Model Year')
    data['CO2-to-MPG Ratio'] = data['Yearly Sustainability Score'] / data['Model Year']

    plt.figure(figsize=(12, 7), facecolor='black')
    plt.plot(data['Model Year'], data['CO2-to-MPG Ratio'], marker='o', color='cyan', linewidth=2)
    configure_plot("Year", "CO2-to-MPG Ratio")
    plt.savefig(f"{plots_dir}/{manufacturer}_co2_to_mpg_ratio.png", dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()

# 5. **Comparative Boxplot for Sustainability Scores**
plt.figure(figsize=(14, 8), facecolor='black')
aggregated_scores.boxplot(
    by='Manufacturer',
    column=['Yearly Sustainability Score'],
    grid=False,
    patch_artist=True,
    boxprops=dict(facecolor='cyan', color='white'),
    medianprops=dict(color='white'),
    whiskerprops=dict(color='white'),
    capprops=dict(color='white'),
    flierprops=dict(marker='o', color='white', alpha=0.5),
)
configure_plot("Manufacturer", "Sustainability Score")
plt.xticks(rotation=45)
plt.savefig(f"{plots_dir}/comparative_sustainability_boxplot.png", dpi=300, facecolor='black', bbox_inches='tight')
plt.close()

print("All visuals have been successfully generated.")