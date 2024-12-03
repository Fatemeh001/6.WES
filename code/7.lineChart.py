
import pandas as pd
import lightningchart as lc
import random

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

datasets = {
    "Perth_49": "dataset/WEC_Perth_49.csv",
    "Perth_100": "dataset/WEC_Perth_100.csv",
    "Sydney_49": "dataset/WEC_Sydney_49.csv",
    "Sydney_100": "dataset/WEC_Sydney_100.csv"
}

styles = {
    "Perth_49": {"color": lc.Color('blue'), "point_shape": "circle"},
    "Sydney_49": {"color": lc.Color('red'), "point_shape": "triangle"},
    "Perth_100": {"color": lc.Color('orange'), "point_shape": "square"},
    "Sydney_100": {"color": lc.Color('green'), "point_shape": "diamond"}
}

chart = lc.ChartXY(
    theme=lc.Themes.Dark,
    title="q-factor performance for different buoy layouts with Points"
)

chart.get_default_x_axis().set_title("Buoy Number")
chart.get_default_y_axis().set_title("q-factor")

for name, filepath in datasets.items():
    data = pd.read_csv(filepath)
    buoy_numbers = []
    q_factors = []
    remaining_buoys = data.filter(like='Power')
    total_power = data['Total_Power'].iloc[0]
    
    while not remaining_buoys.empty:
        individual_power_sum = remaining_buoys.sum(axis=1).iloc[0]
        q_factors.append(total_power / individual_power_sum)
        buoy_numbers.append(len(remaining_buoys.columns))
        min_power_buoy = remaining_buoys.iloc[0].idxmin()
        remaining_buoys = remaining_buoys.drop(columns=[min_power_buoy])
    
    series = chart.add_point_line_series()
    series.set_name(name)
    series.set_point_shape(styles[name]["point_shape"])
    series.set_point_size(8)
    series.set_point_color(styles[name]["color"])
    series.set_line_thickness(2)
    series.set_line_color(styles[name]["color"])
    series.add(x=buoy_numbers, y=q_factors)

chart.add_legend().add(chart)
chart.open()
