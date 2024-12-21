import matplotlib.pyplot as plt
import seaborn as sns
from data_processing import specific_manufacturers_filtered

# Real-World CO2 Emissions by Manufacturer
def plot_co2_emissions():
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=specific_manufacturers_filtered, x="Model Year", y="Real-World CO2 (g/mi)", hue="Manufacturer", marker='o')
    plt.title("Real-World CO2 Emissions by Manufacturer (2008-2023)", fontsize=16)
    plt.xlabel("Model Year", fontsize=14)
    plt.ylabel("CO2 Emissions (g/mi)", fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Manufacturer")
    plt.xticks(rotation=45)
    plt.yticks(fontsize=12)  # Ensure y-axis values are displayed clearly
    plt.tight_layout()
    plt.show()

# Call the function to generate the plot
plot_co2_emissions()