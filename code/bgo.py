import pandas as pd
import numpy as np
import csv
from sko.GA import GA
from sko.DE import DE
from sko.PSO import PSO

files = {
    "WEC_Perth_49.csv": "Perth_49",
    "WEC_Perth_100.csv": "Perth_100",
    "WEC_Sydney_49.csv": "Sydney_49",
    "WEC_Sydney_100.csv": "Sydney_100"
}

def objective_function(positions, power_columns, data):
    total_power = 0
    for idx, (x, y) in enumerate(positions.reshape(-1, 2)):
        power_column = power_columns[idx]
        total_power += data[power_column].iloc[0]
    return -total_power

def run_bga(objective_function, bounds, power_columns, data, max_iter=100):
    n_dim = len(bounds)
    ga = GA(func=lambda x: objective_function(x, power_columns, data),
            n_dim=n_dim, size_pop=50, max_iter=max_iter, prob_mut=0.1)
    best_x, best_y = ga.run()
    return best_x.reshape(-1, 2), -best_y

def run_bde(objective_function, bounds, power_columns, data, max_iter=100):
    n_dim = len(bounds)
    de = DE(func=lambda x: objective_function(x, power_columns, data),
            n_dim=n_dim, size_pop=50, max_iter=max_iter)
    best_x, best_y = de.run()
    return best_x.reshape(-1, 2), -best_y

def run_bpso(objective_function, bounds, power_columns, data, max_iter=100):
    n_dim = len(bounds)
    pso = PSO(func=lambda x: objective_function(x, power_columns, data),
              n_dim=n_dim, pop=50, max_iter=max_iter)
    best_x, best_y = pso.run()
    return best_x.reshape(-1, 2), -best_y

all_results = []

for file_path, dataset_name in files.items():
    data = pd.read_csv(f"dataset/{file_path}")
    power_columns = [col for col in data.columns if 'Power' in col]
    bounds = [(0, 1000) for _ in range(len(power_columns) * 2)]
    
    best_positions_bga, best_power_bga = run_bga(objective_function, bounds, power_columns, data)
    best_positions_bde, best_power_bde = run_bde(objective_function, bounds, power_columns, data)
    best_positions_bpso, best_power_bpso = run_bpso(objective_function, bounds, power_columns, data)
    
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "bGA",
        "Best Layout": best_positions_bga.tolist(),
        "Maximized Power": best_power_bga
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "bDE",
        "Best Layout": best_positions_bde.tolist(),
        "Maximized Power": best_power_bde
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "bPSO",
        "Best Layout": best_positions_bpso.tolist(),
        "Maximized Power": best_power_bpso
    })

with open('results_binary_combined.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Dataset", "Algorithm", "Best Layout", "Maximized Power"])
    writer.writeheader()
    writer.writerows(all_results)

print("All results saved to 'results_binary_combined.csv'")
