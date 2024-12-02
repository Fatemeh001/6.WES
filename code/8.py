import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
data = {
    "Perth 49-buoy": "dataset/WEC_Perth_49.csv",
#     "Perth 100-buoy": "dataset/WEC_Perth_100.csv",
#     "Sydney 49-buoy": "dataset/WEC_Sydney_49.csv",
#     "Sydney 100-buoy": "dataset/WEC_Sydney_100.csv"
}

# Process each file and create scatter plot
num_buoys = 49
X_cols = [f"X{i}" for i in range(1, num_buoys + 1)]
Y_cols = [f"Y{i}" for i in range(1, num_buoys + 1)]
Power_cols = [f"Power{i}" for i in range(1, num_buoys + 1)]

X = data[X_cols].values.flatten()
Y = data[Y_cols].values.flatten()
Power = data[Power_cols].values.flatten()

# Create a scatter plot
plt.figure(figsize=(8, 6))
sc = plt.scatter(X, Y, c=Power, cmap="viridis", edgecolor='k')
plt.colorbar(sc, label="Power (W)")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title("49-buoy Layout Power Distribution")
plt.grid(True)
plt.show()