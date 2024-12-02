# import pandas as pd
# import lightningchart as lc
# import numpy as np

# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# file_path = 'optimization_results.xlsx'
# data = pd.read_excel(file_path)

# data['Maximized Power'] = pd.to_numeric(data['Maximized Power'], errors='coerce')  
# filtered_data = data[
#     (data['Maximized Power'] > 0) &
#     (data['Algorithm'].notnull())
# ]

# algorithms = filtered_data['Algorithm'].unique()
# datasets = filtered_data['Dataset'].unique()

# chart = lc.Chart3D(
#     theme=lc.Themes.Dark,
#     title="Algorithm Performance on Datasets"
# )

# chart.get_default_x_axis().set_title("Dataset")
# chart.get_default_y_axis().set_title("Maximized Power")
# chart.get_default_z_axis().set_title("Algorithm")

# x_axis = chart.get_default_x_axis()
# x_axis.set_interval(0, len(datasets) - 1)
# x_axis.set_tick_strategy('Empty')

# for i, dataset in enumerate(datasets):
#     tick = x_axis.add_custom_tick()
#     tick.set_value(float(i))
#     tick.set_text(dataset)

# z_axis = chart.get_default_z_axis()
# z_axis.set_interval(0, len(algorithms) - 1)
# z_axis.set_tick_strategy('Empty')

# for i, algorithm in enumerate(algorithms):
#     tick = z_axis.add_custom_tick()
#     tick.set_value(float(i))
#     tick.set_text(algorithm)

# box_series = chart.add_box_series()

# color = box_series.set_palette_coloring(
#     steps=[
#         {'value': 0.0, 'color': lc.Color('blue')},
#         {'value': 0.25, 'color': lc.Color('yellow')},
#         {'value': 0.5, 'color': lc.Color('green')},
#         {'value': 0.75, 'color': lc.Color('orange')},
#         {'value': 1.0, 'color': lc.Color('red')}
#     ],
#     percentage_values=True,
#     look_up_property='y'
# )
# chart.add_legend().add(color)

# def generate_static_boxes(algorithms, datasets):
#     boxes = []
#     for i, algorithm in enumerate(algorithms):
#         for j, dataset in enumerate(datasets):
#             total_value = filtered_data[
#                 (filtered_data['Algorithm'] == algorithm) &
#                 (filtered_data['Dataset'] == dataset)
#             ]['Maximized Power'].sum()
#             boxes.append({
#                 'xCenter': float(j),
#                 'yCenter': float(total_value) / 2,
#                 'zCenter': i,
#                 'xSize': 0.5,
#                 'ySize': float(total_value),
#                 'zSize': 0.5
#             })
#     return boxes

# box_series.set_rounded_edges(0.4)

# static_boxes = generate_static_boxes(algorithms, datasets)
# box_series.add(static_boxes)

# chart.open()



import pandas as pd
import lightningchart as lc
import numpy as np

# Load license
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load dataset
file_path = 'optimization_results.xlsx'
data = pd.read_excel(file_path)

# Transform and filter data
filtered_data = data.melt(id_vars=['Dataset'], var_name='Algorithm', value_name='Maximized Power')
filtered_data['Maximized Power'] = pd.to_numeric(filtered_data['Maximized Power'], errors='coerce').abs()  # Convert to positive
filtered_data = filtered_data[(filtered_data['Maximized Power'] > 0) & (filtered_data['Algorithm'].notnull())]

# Select top 5 datasets based on total maximized power
top_datasets = (
    filtered_data.groupby('Dataset')['Maximized Power'].sum()
    .sort_values(ascending=False)
    .head(5).index
)
filtered_data = filtered_data[filtered_data['Dataset'].isin(top_datasets)]

# Extract unique algorithms and datasets
algorithms = [alg for alg in filtered_data['Algorithm'].unique()]
datasets = sorted(top_datasets)

# Initialize the chart
chart = lc.Chart3D(
    theme=lc.Themes.Dark,
    title="Top 5 Datasets by Total Maximized Power (Positive Values)"
)

# Configure axes
x_axis = chart.get_default_x_axis()
y_axis = chart.get_default_y_axis()
z_axis = chart.get_default_z_axis()

x_axis.set_title("Dataset")
y_axis.set_title("Maximized Power (Absolute)")
z_axis.set_title("Algorithm")

x_axis.set_interval(0, len(datasets) - 1)
x_axis.set_tick_strategy('Empty')

for i, dataset in enumerate(datasets):
    tick = x_axis.add_custom_tick()
    tick.set_value(float(i))
    tick.set_text(dataset)

z_axis.set_interval(0, len(algorithms) - 1)
z_axis.set_tick_strategy('Empty')

for i, algorithm in enumerate(algorithms):
    tick = z_axis.add_custom_tick()
    tick.set_value(float(i))
    tick.set_text(algorithm)

# Add a box series
box_series = chart.add_box_series()

# Configure coloring
color = box_series.set_palette_coloring(
    steps=[
        {'value': 0.0, 'color': lc.Color('blue')},
        {'value': 0.25, 'color': lc.Color('yellow')},
        {'value': 0.5, 'color': lc.Color('green')},
        {'value': 0.75, 'color': lc.Color('orange')},
        {'value': 1.0, 'color': lc.Color('red')}
    ],
    percentage_values=True,
    look_up_property='y'
)
chart.add_legend().add(color)

# Generate the static boxes
def generate_static_boxes(algorithms, datasets):
    boxes = []
    for i, algorithm in enumerate(algorithms):
        for j, dataset in enumerate(datasets):
            total_value = filtered_data[
                (filtered_data['Algorithm'] == algorithm) & 
                (filtered_data['Dataset'] == dataset)
            ]['Maximized Power'].sum()
            boxes.append({
                'xCenter': float(j),
                'yCenter': float(total_value) / 2,
                'zCenter': i,
                'xSize': 0.75,
                'ySize': float(total_value),
                'zSize': 1
            })
    return boxes

box_series.set_rounded_edges(0.4)
static_boxes = generate_static_boxes(algorithms, datasets)
box_series.add(static_boxes)

# Open the chart
chart.open()
