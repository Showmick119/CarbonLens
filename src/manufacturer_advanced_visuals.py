import pandas as pd
import os
import matplotlib.pyplot as plt
from random_forest_model import aggregated_scores

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
    plt.tight_layout()
    fig.savefig(f"{plots_dir}/{manufacturer}_mpg_growth_rate.png", dpi=300, transparent=True, bbox_inches='tight')
    plt.close(fig)

# 3. **Top Manufacturers in Sustainability Efforts**
cumulative_improvement = aggregated_scores.groupby('Manufacturer')['Yearly Sustainability Score'].sum().sort_values()
fig, ax = plt.subplots(figsize=(12, 5))
ax.barh(
    cumulative_improvement.index,
    cumulative_improvement.values,
    color='cyan',
    edgecolor='white'
)
ax.set_facecolor('none')  # Transparent background
fig.patch.set_alpha(0)
ax.set_xlabel("Cumulative Improvement", fontsize=12, color='white')
ax.set_ylabel("Manufacturer", fontsize=12, color='white')
ax.tick_params(axis='x', colors='white', labelsize=10)
ax.tick_params(axis='y', colors='white', labelsize=10)
plt.tight_layout()
fig.savefig(f"{plots_dir}/top_sustainability_efforts.png", dpi=300, transparent=True, bbox_inches='tight')
plt.close(fig)

# 4. **Comparative Boxplot for Sustainability Scores**
fig, ax = plt.subplots(figsize=(12, 5))
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
    ax=ax
)
ax.set_facecolor('none')  # Transparent background
fig.patch.set_alpha(0)
ax.tick_params(axis='x', colors='white', labelsize=10, rotation=45)
ax.tick_params(axis='y', colors='white', labelsize=10)
plt.tight_layout()
fig.savefig(f"{plots_dir}/comparative_sustainability_boxplot.png", dpi=300, transparent=True, bbox_inches='tight')
plt.close(fig)

print("All advanced visuals have been successfully updated.")