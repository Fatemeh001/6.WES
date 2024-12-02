
import pandas as pd
import lightningchart as lc
import numpy as np

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/data.xlsx'
data = pd.read_excel(file_path)

columns_to_normalize = data.columns[1:]
for col in columns_to_normalize:
    data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())

regions = columns_to_normalize
algorithms = data["Algorithm"]

chart = lc.Chart3D(
    theme=lc.Themes.Dark,
    title="Normalized Values for Algorithms Across Regions"
)

chart.set_bounding_box(1, 0.8, 4)

chart.get_default_x_axis().set_title("Region")
chart.get_default_y_axis().set_title("Normalized Value")
chart.get_default_z_axis().set_title("Algorithm")

x_axis = chart.get_default_x_axis()
x_axis.set_interval(0, len(regions) - 1)
x_axis.set_tick_strategy('Empty')

for i, region in enumerate(regions):
    tick = x_axis.add_custom_tick()
    tick.set_value(float(i))
    tick.set_text(region)

z_axis = chart.get_default_z_axis()
z_axis.set_interval(0, len(algorithms) - 1)
z_axis.set_tick_strategy('Empty')

for i, algorithm in enumerate(algorithms):
    tick = z_axis.add_custom_tick()
    tick.set_value(float(i))
    tick.set_text(algorithm)

box_series = chart.add_box_series()

color = box_series.set_palette_coloring(
    steps=[
        {'value': 0.0, 'color': lc.Color(22, 14, 138)}, 
        {'value': 0.25, 'color': lc.Color(5, 229, 245)},
        {'value': 0.5, 'color': lc.Color(238, 255, 5)},
        {'value': 0.75, 'color': lc.Color(255, 113, 5)},
        {'value': 1.0, 'color': lc.Color(212, 2, 2)}
    ],
    percentage_values=True,
    look_up_property='y'
)
chart.add_legend().add(color)

def generate_boxes(data, algorithms, regions):
    boxes = []
    for i, algorithm in enumerate(algorithms):
        for j, region in enumerate(regions):
            value = data.loc[i, region]
            boxes.append({
                'xCenter': float(j),
                'yCenter': value / 2,
                'zCenter': float(i),
                'xSize': 0.8,
                'ySize': value,
                'zSize': 0.8
            })
    return boxes


static_boxes = generate_boxes(data, algorithms, regions)
box_series.add(static_boxes)

chart.open()

