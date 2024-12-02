
# import lightningchart as lc
# import pandas as pd
# import numpy as np

# # Load your LightningChart license
# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the datasets
# file_path_49 = 'dataset/WEC_Perth_49.csv'
# file_path_100 = 'dataset/WEC_Perth_100.csv'

# data_49 = pd.read_csv(file_path_49)
# data_100 = pd.read_csv(file_path_100)

# # Prepare data for WEC_Perth_49
# powers_49_filtered = data_49.filter(like="Power").drop(columns=["Total_Power"], errors='ignore').mean()
# coordinates_49_filtered = [int(col.replace("Power", "")) for col in powers_49_filtered.index]
# power_values_49 = np.array(powers_49_filtered)
# grid_x_49, grid_y_49 = np.meshgrid(coordinates_49_filtered, coordinates_49_filtered)
# z_values_49 = np.outer(power_values_49, power_values_49)

# # Prepare data for WEC_Perth_100
# powers_100_filtered = data_100.filter(like="Power").drop(columns=["Total_Power"], errors='ignore').mean()
# coordinates_100_filtered = [int(col.replace("Power", "")) for col in powers_100_filtered.index]
# power_values_100 = np.array(powers_100_filtered)
# grid_x_100, grid_y_100 = np.meshgrid(coordinates_100_filtered, coordinates_100_filtered)
# z_values_100 = np.outer(power_values_100, power_values_100)

# # Initialize the dashboard
# dashboard = lc.Dashboard(columns=2, rows=1, theme=lc.Themes.Light)

# # Create Heatmap for WEC_Perth_49
# chart_49 = dashboard.ChartXY(
#     title="Heatmap: Power Distribution (WEC_Perth_49)",
#     column_index=0,
#     row_index=0
# )
# heatmap_49 = chart_49.add_heatmap_grid_series(
#     rows=len(coordinates_49_filtered),
#     columns=len(coordinates_49_filtered)
# )
# heatmap_49.set_start(x=0, y=0)
# heatmap_49.set_end(x=len(coordinates_49_filtered), y=len(coordinates_49_filtered))
# heatmap_49.set_intensity_interpolation(True)
# heatmap_49.invalidate_intensity_values(z_values_49.tolist())
# heatmap_49.set_palette_coloring(
#     steps=[
#         {"value": np.min(z_values_49), "color": lc.Color('blue')},
#         {"value": np.percentile(z_values_49, 25), "color": lc.Color('cyan')},
#         {"value": np.median(z_values_49), "color": lc.Color('green')},
#         {"value": np.percentile(z_values_49, 75), "color": lc.Color('yellow')},
#         {"value": np.max(z_values_49), "color": lc.Color('red')}
#     ],
#     look_up_property="value",
#     interpolate=True
# )
# heatmap_49.hide_wireframe()

# # Create Heatmap for WEC_Perth_100
# chart_100 = dashboard.ChartXY(
#     title="Heatmap: Power Distribution (WEC_Perth_100)",
#     column_index=1,
#     row_index=0
# )
# heatmap_100 = chart_100.add_heatmap_grid_series(
#     rows=len(coordinates_100_filtered),
#     columns=len(coordinates_100_filtered)
# )
# heatmap_100.set_start(x=0, y=0)
# heatmap_100.set_end(x=len(coordinates_100_filtered), y=len(coordinates_100_filtered))
# heatmap_100.set_intensity_interpolation(True)
# heatmap_100.invalidate_intensity_values(z_values_100.tolist())
# heatmap_100.set_palette_coloring(
#     steps=[
#         {"value": np.min(z_values_100), "color": lc.Color('blue')},
#         {"value": np.percentile(z_values_100, 25), "color": lc.Color('cyan')},
#         {"value": np.median(z_values_100), "color": lc.Color('green')},
#         {"value": np.percentile(z_values_100, 75), "color": lc.Color('yellow')},
#         {"value": np.max(z_values_100), "color": lc.Color('red')}
#     ],
#     look_up_property="value",
#     interpolate=True
# )
# heatmap_100.hide_wireframe()

# # Open the dashboard
# dashboard.open()



import lightningchart as lc
import pandas as pd
import numpy as np

# Load your LightningChart license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'dataset/WEC_Perth_49.csv'
data_49 = pd.read_csv(file_path)

# Extract X, Y, and Power columns
x = data_49['X1']  # Replace 'X1' with the actual column for X-coordinates
y = data_49['Y1']  # Replace 'Y1' with the actual column for Y-coordinates
power = data_49['Power1']  # Replace 'Power1' with the actual column for power

# Create unique X and Y coordinates
x_unique = np.unique(x)
y_unique = np.unique(y)

# Initialize a 2D grid for Heatmap
z_values = np.zeros((len(y_unique), len(x_unique)))

# Map power values to the corresponding grid
for i, x_val in enumerate(x_unique):
    for j, y_val in enumerate(y_unique):
        mask = (x == x_val) & (y == y_val)
        if mask.any():
            z_values[j, i] = power[mask].mean()

# Initialize Heatmap
chart = lc.ChartXY(
    title="Spatial Heatmap: Power Distribution",
    theme=lc.Themes.Light,
)

# Add Heatmap grid series
heatmap = chart.add_heatmap_grid_series(
    rows=z_values.shape[0],
    columns=z_values.shape[1],
)
heatmap.set_start(x=x_unique.min(), y=y_unique.min())
heatmap.set_end(x=x_unique.max(), y=y_unique.max())
heatmap.set_intensity_interpolation(True)
heatmap.invalidate_intensity_values(z_values.tolist())

# Customize color palette
heatmap.set_palette_coloring(
    steps=[
        {"value": np.min(z_values), "color": lc.Color('blue')},
        {"value": np.percentile(z_values, 25), "color": lc.Color('cyan')},
        {"value": np.median(z_values), "color": lc.Color('green')},
        {"value": np.percentile(z_values, 75), "color": lc.Color('yellow')},
        {"value": np.max(z_values), "color": lc.Color('red')}
    ],
    look_up_property="value",
    interpolate=True,
)
heatmap.hide_wireframe()

# Set axis titles
chart.get_default_x_axis().set_title("X-coordinates")
chart.get_default_y_axis().set_title("Y-coordinates")

# Open the chart
chart.open()
