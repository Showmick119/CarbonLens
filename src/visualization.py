import matplotlib.pyplot as plt
import seaborn as sns
from data_processing import specific_manufacturers_filtered

# Real-World CO2 Emissions by Manufacturer
def plot_co2_emissions():
    plt.figure(figsize=(12, 6))
    
    # Lineplot
    sns.lineplot(
        data=specific_manufacturers_filtered,
        x="Model Year",
        y="Real-World CO2 (g/mi)",
        hue="Manufacturer",
        marker='o'
    )
    
    # Manually set x-axis and y-axis ticks
    plt.xticks(ticks=range(2008, 2024, 2), fontsize=12)  # X-axis: every 2 years from 2008 to 2023
    plt.yticks(ticks=range(0, 500, 50), fontsize=12)  # Y-axis: from 0 to 500 in increments of 50
    
    # Axis Labels and Title
    plt.title("Real-World CO2 Emissions by Manufacturer (2008-2023)", fontsize=16)
    plt.xlabel("Model Year", fontsize=14)
    plt.ylabel("CO2 Emissions (g/mi)", fontsize=14)
    
    # Additional Styling
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Manufacturer")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Call the function to generate the plot
plot_co2_emissions()
