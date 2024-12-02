import pandas as pd
import matplotlib.pyplot as plt

# Load datasets (replace with actual file paths)
datasets = {
    "Perth_49": "dataset/WEC_Perth_49.csv",
    "Perth_100": "dataset/WEC_Perth_100.csv",
    "Sydney_49": "dataset/WEC_Sydney_49.csv",
    "Sydney_100": "dataset/WEC_Sydney_100.csv"
}



# Define colors and markers for each dataset
styles = {
    "Perth_49": {"color": "blue", "marker": "o", "linestyle": "-"},
    "Sydney_49": {"color": "red", "marker": "o", "linestyle": "-"},
    "Perth_100": {"color": "orange", "marker": None, "linestyle": "--"},
    "Sydney_100": {"color": "green", "marker": None, "linestyle": "--"}
}

plt.figure(figsize=(10, 6))

# Iterate through datasets
for name, filepath in datasets.items():
    # Load data
    data = pd.read_csv(filepath)
    
    # Initialize q-factor calculation
    buoy_numbers = []
    q_factors = []
    
    # Iteratively remove lowest-power buoy
    remaining_buoys = data.filter(like='Power')  # Filter power columns
    total_power = data['Total_Power'].iloc[0]  # Initial total power
    while not remaining_buoys.empty:
        # Calculate q-factor
        individual_power_sum = remaining_buoys.sum(axis=1).iloc[0]
        q_factors.append(total_power / individual_power_sum)
        buoy_numbers.append(len(remaining_buoys.columns))
        
        # Remove lowest-power buoy
        min_power_buoy = remaining_buoys.iloc[0].idxmin()
        remaining_buoys = remaining_buoys.drop(columns=[min_power_buoy])
    
    # Plot
    plt.plot(buoy_numbers, q_factors, label=name, **styles[name])

# Configure plot
plt.xlabel("Buoy Number", fontsize=12)
plt.ylabel("q-factor", fontsize=12)
plt.title("q-factor performance for different buoy layouts", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()