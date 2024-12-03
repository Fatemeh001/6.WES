import pandas as pd
import numpy as np
import lightningchart as lc
from scipy.interpolate import griddata

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/wec_Sydney_49.csv'
data = pd.read_csv(file_path)

x = data['X1']
y = data['Y1']
power = data['Power1']

X_grid, Y_grid = np.meshgrid(
    np.linspace(x.min(), x.max(), 49),
    np.linspace(y.min(), y.max(), 49)
)

Z_grid = griddata((x, y), power, (X_grid, Y_grid), method='cubic')
Z_grid[np.isnan(Z_grid)] = np.nanmean(power)

chart = lc.Chart3D(
    theme=lc.Themes.Black,
    title='Power Distribution: Sydney Wave Scenario (49 Buoy)'
)

surface_series = chart.add_surface_grid_series(
    columns=Z_grid.shape[1],
    rows=Z_grid.shape[0]
)

surface_series.set_start(x=x.min(), z=y.min())
surface_series.set_end(x=x.max(), z=y.max())
surface_series.set_step(
    x=(x.max() - x.min()) / Z_grid.shape[1],
    z=(y.max() - y.min()) / Z_grid.shape[0]
)

surface_series.invalidate_height_map(Z_grid.tolist())
surface_series.invalidate_intensity_values(Z_grid.tolist())

surface_series.set_color_shading_style(phong_shading=True, specular_reflection=0.3)

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

chart.get_default_x_axis().set_title('X (m)')
chart.get_default_y_axis().set_title('Y (m)')
chart.get_default_z_axis().set_title('Power (W)')

chart.set_background_color(lc.Color(0, 0, 0))

chart.add_legend(data=surface_series)

chart.open()
