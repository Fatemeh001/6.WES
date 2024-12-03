# import pandas as pd
# import numpy as np
# import lightningchart as lc

# # بارگذاری لایسنس
# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # بارگذاری داده‌ها
# file_path = 'dataset/WEC_Perth_49.csv'
# data = pd.read_csv(file_path)

# # استخراج ستون‌های X، Y و Power
# x_columns = [col for col in data.columns if col.startswith('X')]
# y_columns = [col for col in data.columns if col.startswith('Y')]
# power_columns = [col for col in data.columns if col.startswith('Power')]

# # آماده‌سازی داده‌ها
# x_values = data[x_columns].values.flatten()
# y_values = data[y_columns].values.flatten()
# power_values = data[power_columns].values.flatten()

# # ایجاد نمودار سه‌بعدی
# chart3d = lc.Chart3D(title="Power Landscape", theme=lc.Themes.Dark)

# # اضافه کردن سری نقاط سه‌بعدی
# point_series = chart3d.add_point_series()
# point_series.add(
#     x=x_values,
#     y=y_values,
#     z=power_values
# )

# # تنظیمات محورها
# chart3d.get_default_x_axis().set_title("X Position (m)")
# chart3d.get_default_y_axis().set_title("Y Position (m)")
# chart3d.get_default_z_axis().set_title("Power Output (kW)")

# # باز کردن نمودار سه‌بعدی
# chart3d.open()

# # ایجاد نمودار Heatmap
# heatmap_chart = lc.ChartXY(title="Heatmap of Power Output", theme=lc.Themes.Light)
# heatmap_series = heatmap_chart.add_point_series(data_2d=power_values.reshape(len(x_columns), len(y_columns)))
# heatmap_chart.get_default_x_axis().set_title("X Position (m)")
# heatmap_chart.get_default_y_axis().set_title("Y Position (m)")

# # باز کردن نمودار Heatmap
# heatmap_chart.open()


import lightningchart as lc
import pandas as pd

# بارگذاری لایسنس
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# بارگذاری داده‌ها
file_path = 'dataset/WEC_Perth_49.csv'  # مسیر فایل خود را وارد کنید
data = pd.read_csv(file_path)

# استخراج داده‌ها
x_columns = [col for col in data.columns if col.startswith('X')]
y_columns = [col for col in data.columns if col.startswith('Y')]
power_columns = [col for col in data.columns if col.startswith('Power')]

# آماده‌سازی داده‌ها
x_values = data[x_columns].values.flatten()
y_values = data[y_columns].values.flatten()
power_values = data[power_columns].values.flatten()

# فیلتر کردن داده‌ها
filtered_indices = power_values >= 1000
x_filtered = x_values[filtered_indices]
y_filtered = y_values[filtered_indices]
power_filtered = power_values[filtered_indices]

# دیباگ داده‌های فیلتر شده
print("Filtered X:", x_filtered)
print("Filtered Y:", y_filtered)
print("Filtered Power:", power_filtered)

# ایجاد نمودار سه‌بعدی
chart = lc.Chart3D(
    theme=lc.Themes.Light,
    title='3D Power Distribution'
)

# اضافه کردن سری نقاط سه‌بعدی
series = chart.add_point_series(
    render_2d=False,
    individual_lookup_values_enabled=True,
    individual_point_color_enabled=True,
    individual_point_size_enabled=True,
)

# تنظیم شکل و پالت رنگی نقاط
series.set_point_shape('sphere')
series.set_palette_point_colors(
    steps=[
        {'value': power_filtered.min(), 'color': lc.Color('blue')},
        {'value': (power_filtered.min() + power_filtered.max()) / 2, 'color': lc.Color('green')},
        {'value': power_filtered.max(), 'color': lc.Color('red')},
    ],
    look_up_property='value',
    interpolate=True,
    percentage_values=False
)

# افزودن داده‌ها
if len(x_filtered) > 0 and len(y_filtered) > 0 and len(power_filtered) > 0:
    data_points = [
        {
            'x': x,
            'y': y,
            'z': power,
            'size': 8,
            'value': power  # برای اعمال رنگ‌بندی
        }
        for x, y, power in zip(x_filtered, y_filtered, power_filtered)
    ]
    series.add(data_points)
else:
    print("No valid data points to add.")

# تنظیمات محورها
x_axis = chart.get_default_x_axis()
x_axis.set_title("X Position (m)")
x_axis.set_interval(x_filtered.min(), x_filtered.max())  # تنظیم محدوده محور X

y_axis = chart.get_default_y_axis()
y_axis.set_title("Y Position (m)")
y_axis.set_interval(y_filtered.min(), y_filtered.max())  # تنظیم محدوده محور Y

z_axis = chart.get_default_z_axis()
z_axis.set_title("Power Output (kW)")
z_axis.set_interval(power_filtered.min(), power_filtered.max())  # تنظیم محدوده محور Z

# فعال کردن تعاملات
chart.set_mouse_interaction_rotate(True)
chart.set_mouse_interaction_zoom(True)

# باز کردن نمودار
chart.open()
