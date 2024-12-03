import pandas as pd
import numpy as np
import lightningchart as lc
from scipy.interpolate import griddata

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

def create_surface_chart(chart, title, x, y, power, grid_size):
    X_grid, Y_grid = np.meshgrid(
        np.linspace(x.min(), x.max(), grid_size),
        np.linspace(y.min(), y.max(), grid_size)
    )
    Z_grid = griddata((x, y), power, (X_grid, Y_grid), method='cubic')
    Z_grid[np.isnan(Z_grid)] = np.nanmean(power)
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
    color= surface_series.set_palette_coloring(
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
    chart.set_title(title)
    chart.get_default_x_axis().set_title('X (m)')
    chart.get_default_y_axis().set_title('Y (m)')
    chart.get_default_z_axis().set_title('Power (W)')
    
    chart.add_legend().add(color)

file_paths = [
    ('Power Distribution: Perth Wave (49 Buoy)', 'dataset/WEC_Perth_49.csv', 49),
    ('Power Distribution: Sydney Wave (49 Buoy)', 'dataset/wec_Sydney_49.csv', 49),
    ('Power Distribution: Perth Wave (100 Buoy)', 'dataset/WEC_Perth_100.csv', 100),
    ('Power Distribution: Sydney Wave (100 Buoy)', 'dataset/WEC_Sydney_100.csv', 100)
]

dashboard = lc.Dashboard(columns=2, rows=2, theme=lc.Themes.Black)

for i, (title, file_path, grid_size) in enumerate(file_paths):
    data = pd.read_csv(file_path)
    x = data['X1']
    y = data['Y1']
    power = data['Power1']
    chart = dashboard.Chart3D(column_index=i % 2, row_index=i // 2)
    create_surface_chart(chart, title, x, y, power, grid_size)

dashboard.open()
