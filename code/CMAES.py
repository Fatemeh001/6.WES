import pandas as pd
import numpy as np
import csv
from cma import CMAEvolutionStrategy

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

def cmaes_algorithm(objective_function, bounds, power_columns, data, max_iter=100):
    initial_point = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    sigma = 0.5
    es = CMAEvolutionStrategy(initial_point, sigma)
    for _ in range(max_iter):
        solutions = es.ask()
        fitness = [objective_function(np.array(sol), power_columns, data) for sol in solutions]
        es.tell(solutions, fitness)
        if es.stop():
            break
    return es.result.xbest, -es.result.fbest

def cmaes_2plus2_algorithm(objective_function, bounds, power_columns, data, max_iter=100):
    initial_point = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    sigma = 0.5
    es = CMAEvolutionStrategy(initial_point, sigma, {'popsize': 2})  # تغییر اندازه جمعیت به 2+2
    for _ in range(max_iter):
        solutions = es.ask()
        fitness = [objective_function(np.array(sol), power_columns, data) for sol in solutions]
        es.tell(solutions, fitness)
        if es.stop():
            break
    return es.result.xbest, -es.result.fbest

all_results = []

for file_path, dataset_name in files.items():
    data = pd.read_csv(f"dataset/{file_path}")
    power_columns = [col for col in data.columns if 'Power' in col]
    bounds = [(0, 1000) for _ in range(len(power_columns) * 2)]
    
    best_positions_cmaes, best_power_cmaes = cmaes_algorithm(objective_function, bounds, power_columns, data)
    best_positions_cmaes_2plus2, best_power_cmaes_2plus2 = cmaes_2plus2_algorithm(objective_function, bounds, power_columns, data)
    
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "CMAES",
        "Best Layout": best_positions_cmaes.tolist(),
        "Maximized Power": best_power_cmaes
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "2+2 CMAES",
        "Best Layout": best_positions_cmaes_2plus2.tolist(),
        "Maximized Power": best_power_cmaes_2plus2
    })

with open('results_cmaes_combined.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Dataset", "Algorithm", "Best Layout", "Maximized Power"])
    writer.writeheader()
    writer.writerows(all_results)

print("All results saved to 'results_cmaes_combined.csv'")
