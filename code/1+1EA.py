import pandas as pd
import numpy as np
import csv

# لیست فایل‌ها و نام دیتاست‌ها
files = {
    "WEC_Perth_49.csv": "Perth_49",
    "WEC_Perth_100.csv": "Perth_100",
    "WEC_Sydney_49.csv": "Sydney_49",
    "WEC_Sydney_100.csv": "Sydney_100"
}

# تعریف تابع هدف
def objective_function(positions, power_columns, data):
    total_power = 0
    for idx, (x, y) in enumerate(positions.reshape(-1, 2)):  # تبدیل آرایه به مختصات
        power_column = power_columns[idx]
        total_power += data[power_column].iloc[0]  # استفاده از توان مرتبط با هر بویه
    return -total_power  # برای ماکزیمم کردن، منفی می‌شود

# الگوریتم 1+1 EA
def evolutionary_algorithm(objective_function, bounds, power_columns, data, max_iter=100):
    x = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    fx = objective_function(x, power_columns, data)
    
    for _ in range(max_iter):
        candidate = x + np.random.normal(0, 10, size=x.shape)  # جهش
        candidate = np.clip(candidate, [b[0] for b in bounds], [b[1] for b in bounds])
        fcandidate = objective_function(candidate, power_columns, data)
        
        if fcandidate < fx:  # جایگزینی در صورت بهبود
            x, fx = candidate, fcandidate
    
    return x, -fx  # بازگشت بهترین موقعیت و مقدار توان

# ترکیب نتایج برای تمام فایل‌ها
all_results = []

for file_path, dataset_name in files.items():
    print(f"Processing {dataset_name}...")
    
    # بارگذاری داده
    data = pd.read_csv(f"dataset/{file_path}")
    
    # استخراج ستون‌های مربوط به توان
    power_columns = [col for col in data.columns if 'Power' in col]
    
    # تعریف محدوده مختصات برای بویه‌ها
    bounds = [(0, 1000) for _ in range(len(power_columns) * 2)]  # 2 مقدار (X و Y) برای هر بویه
    
    # اجرای الگوریتم
    best_positions, best_power = evolutionary_algorithm(objective_function, bounds, power_columns, data)
    
    # اضافه کردن نتایج به لیست
    all_results.append({
        "Dataset": dataset_name,
        "Best Layout": best_positions.tolist(),
        "Maximized Power": best_power
    })

# ذخیره نتایج در فایل CSV
with open('results_1+1EA_combined.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Dataset", "Best Layout", "Maximized Power"])
    writer.writeheader()
    writer.writerows(all_results)

print("All results saved to 'results_1+1EA_combined.csv'")

