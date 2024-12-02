import pandas as pd
import numpy as np
import lightningchart as lc
from scipy.interpolate import griddata

# Load your LightningChart license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load dataset (WEC_Perth_100.csv)
file_path = 'dataset/WEC_Perth_100.csv'  
data = pd.read_csv(file_path)

# Extract coordinates and power data
x = data['X1']  # Replace 'X1' with actual column for X-coordinates
y = data['Y1']  # Replace 'Y1' with actual column for Y-coordinates
power = data['Power1']  # Replace 'Power1' with actual column for power

# Create a grid for X and Y
X_grid, Y_grid = np.meshgrid(
    np.linspace(x.min(), x.max(), 100),
    np.linspace(y.min(), y.max(), 100)
)

# Interpolate power values onto the grid
Z_grid = griddata((x, y), power, (X_grid, Y_grid), method='cubic')
Z_grid[np.isnan(Z_grid)] = np.nanmean(power)  # Handle NaN values by filling with the mean

# Set up the LightningChart 3D surface chart
chart = lc.Chart3D(
    theme=lc.Themes.Black,
    title='Power Distribution: Perth Wave Scenario (100 Buoy)'
)

surface_series = chart.add_surface_grid_series(
    columns=Z_grid.shape[1],
    rows=Z_grid.shape[0]
)

# Set up dimensions and grid parameters
surface_series.set_start(x=x.min(), z=y.min())
surface_series.set_end(x=x.max(), z=y.max())
surface_series.set_step(
    x=(x.max() - x.min()) / Z_grid.shape[1],
    z=(y.max() - y.min()) / Z_grid.shape[0]
)

# Update height map and intensity values
surface_series.invalidate_height_map(Z_grid.tolist())
surface_series.invalidate_intensity_values(Z_grid.tolist())

# Set color shading for smoother surface
surface_series.set_color_shading_style(phong_shading=True, specular_reflection=0.3)

# Customize palette colors
surface_series.set_palette_coloring(
    steps=[
        {"value": Z_grid.min(), "color": lc.Color('blue')},
        {"value": np.percentile(Z_grid, 25), "color": lc.Color('cyan')},
        {"value": np.median(Z_grid), "color": lc.Color('green')},
        {"value": np.percentile(Z_grid, 75), "color": lc.Color('yellow')},
        {"value": Z_grid.max(), "color": lc.Color('red')}
    ],
    look_up_property='value',
    interpolate=True,
    percentage_values=False
)

# Customize axis labels
chart.get_default_x_axis().set_title('X (m)')
chart.get_default_y_axis().set_title('Y (m)')
chart.get_default_z_axis().set_title('Power (W)')

# Set background color to match Matplotlib style
chart.set_background_color(lc.Color(0, 0, 0))

# Add legend
chart.add_legend(data=surface_series)

# Display chart
chart.open()
