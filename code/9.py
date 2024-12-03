# import lightningchart as lc
# import pandas as pd

# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# file_paths = [
#     'dataset/WEC_Perth_49.csv',
#     'dataset/WEC_Perth_100.csv',
#     'dataset/WEC_Sydney_49.csv',
#     'dataset/WEC_Sydney_100.csv'
# ]

# titles = [
#     "Perth 49 Points",
#     "Perth 100 Points",
#     "Sydney 49 Points",
#     "Sydney 100 Points"
# ]

# dashboard = lc.Dashboard(
#     columns=2,
#     rows=2,
#     theme=lc.Themes.Light
# )

# def create_chart(file_path, title, column_index, row_index):
#     data = pd.read_csv(file_path)

#     x_columns = [f'X{i}' for i in range(1, 50)]
#     y_columns = [f'Y{i}' for i in range(1, 50)]
#     power_columns = [f'Power{i}' for i in range(1, 50)]

#     filtered_data = pd.DataFrame({
#         'X': [data[x].iloc[0] for x in x_columns],
#         'Y': [data[y].iloc[0] for y in y_columns],
#         'Power': [data[p].iloc[0] for p in power_columns]
#     })

#     min_power = filtered_data['Power'].min()
#     max_power = filtered_data['Power'].max()

#     chart = dashboard.ChartXY(
#         title=title,
#         column_index=column_index,
#         row_index=row_index
#     )

#     point_series = chart.add_point_series(
#         lookup_values=True
#     )

#     point_series.set_palette_point_coloring(
#         steps=[
#             {'value': min_power, 'color': lc.Color('blue')},
#             {'value': (min_power + max_power) / 2, 'color': lc.Color('green')},
#             {'value': max_power, 'color': lc.Color('red')}
#         ],
#         look_up_property='value',
#         percentage_values=False
#     )

#     point_series.append_samples(
#         x_values=filtered_data['X'].to_numpy(),
#         y_values=filtered_data['Y'].to_numpy(),
#         lookup_values=filtered_data['Power'].to_numpy()
#     )

#     point_series.set_point_size(10)
#     point_series.set_point_shape('Square')

#     chart.get_default_x_axis().set_title("X (m)")
#     chart.get_default_y_axis().set_title("Y (m)")

# for i, (file_path, title) in enumerate(zip(file_paths, titles)):
#     column_index = i % 2
#     row_index = i // 2
#     create_chart(file_path, title, column_index, row_index)

# dashboard.open()




import lightningchart as lc
import pandas as pd
import numpy as np

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_paths = [
    ('dataset/WEC_Perth_49.csv', "Perth 49 Buoys"),
    ('dataset/WEC_Perth_100.csv', "Perth 100 Buoys"),
    ('dataset/WEC_Sydney_49.csv', "Sydney 49 Buoys"),
    ('dataset/WEC_Sydney_100.csv', "Sydney 100 Buoys")
]

dashboard = lc.Dashboard(
    theme=lc.Themes.Black,
    rows=2,
    columns=3  
)

def create_chart(file_path, title, column_index, row_index, q_factor=None, power=None, alt=False):
    try:
       
        data = pd.read_csv(file_path)

       
        x_columns = [f'X{i}' for i in range(1, 50)]
        y_columns = [f'Y{i}' for i in range(1, 50)]
        power_columns = [f'Power{i}' for i in range(1, 50)]

        filtered_data = pd.DataFrame({
            'X': [data[x].iloc[0] for x in x_columns],
            'Y': [data[y].iloc[0] for y in y_columns],
            'Power': [data[p].iloc[0] for p in power_columns]
        })

       
        if alt:
            filtered_data['X'] += np.random.uniform(-50, 50, size=len(filtered_data['X']))
            filtered_data['Y'] += np.random.uniform(-50, 50, size=len(filtered_data['Y']))
            filtered_data['Power'] *= np.random.uniform(0.9, 1.1, size=len(filtered_data['Power']))
            title += " (Alt Scenario)"

      
        min_power = filtered_data['Power'].min()
        max_power = filtered_data['Power'].max()

       
        full_title = title
        if q_factor is not None and power is not None:
            full_title += f"\nPower={power} W, q-factor={q_factor}"

        
        chart = dashboard.ChartXY(
            title=full_title,
            column_index=column_index,
            row_index=row_index
        )

        
        point_series = chart.add_point_series(
            lookup_values=True
        )

      
        point_series.set_palette_point_coloring(
            steps=[
                {'value': min_power, 'color': lc.Color('blue')},
                {'value': (min_power + max_power) / 2, 'color': lc.Color('green')},
                {'value': max_power, 'color': lc.Color('red')}
            ],
            look_up_property='value',
            percentage_values=False
        )

       
        point_series.append_samples(
            x_values=filtered_data['X'].to_numpy(),
            y_values=filtered_data['Y'].to_numpy(),
            lookup_values=filtered_data['Power'].to_numpy()
        )

       
        point_series.set_point_size(10)
        point_series.set_point_shape('Square')

        
        chart.get_default_x_axis().set_title("X (m)")
        chart.get_default_y_axis().set_title("Y (m)")

    except Exception as e:
        print(f"Error creating chart for {title}: {e}")

create_chart(file_paths[0][0], "Perth 49 Buoys", 0, 0, q_factor=0.8, power=4145252)
create_chart(file_paths[1][0], "Perth 100 Buoys", 1, 0, q_factor=0.76, power=7347403)
create_chart(file_paths[2][0], "Sydney 49 Buoys", 0, 1, q_factor=0.88, power=4177658)
create_chart(file_paths[3][0], "Sydney 100 Buoys", 1, 1, q_factor=0.7, power=7362279)

create_chart(file_paths[0][0], "Perth 49 Buoys", 2, 0, q_factor=0.75, power=7235425, alt=True)
create_chart(file_paths[1][0], "Perth 100 Buoys", 2, 1, q_factor=0.7, power=7337922, alt=True)

dashboard.open()
