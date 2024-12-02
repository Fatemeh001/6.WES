import pandas as pd
import numpy as np
import csv
from scipy.optimize import differential_evolution, minimize

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

def run_de(objective_function, bounds, power_columns, data, max_iter=1000):
    def de_objective_function(positions_flat):
        return objective_function(positions_flat, power_columns, data)
    result = differential_evolution(de_objective_function, bounds, strategy='best1bin', maxiter=max_iter, popsize=15)
    return result.x.reshape(-1, 2), -result.fun

def run_ide(objective_function, bounds, power_columns, data, max_iter=1000):
    def ide_objective_function(positions_flat):
        return objective_function(positions_flat, power_columns, data)
    result = differential_evolution(ide_objective_function, bounds, strategy='rand2bin', maxiter=max_iter, popsize=20)
    return result.x.reshape(-1, 2), -result.fun

def run_ls_nm(objective_function, bounds, power_columns, data, max_iter=1000):
    def ls_nm_objective_function(positions_flat):
        return objective_function(positions_flat, power_columns, data)
    initial_guess = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    result = minimize(ls_nm_objective_function, initial_guess, method='Nelder-Mead', options={'maxiter': max_iter})
    return result.x.reshape(-1, 2), -result.fun

def run_dls_i(objective_function, bounds, power_columns, data, max_iter=100):
    def dls_i_objective_function(positions_flat):
        return objective_function(positions_flat, power_columns, data)
    best_positions = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    best_fitness = dls_i_objective_function(best_positions)
    for _ in range(max_iter):
        candidate = best_positions + np.random.uniform(-10, 10, size=best_positions.shape)
        candidate = np.clip(candidate, [b[0] for b in bounds], [b[1] for b in bounds])
        candidate_fitness = dls_i_objective_function(candidate)
        if candidate_fitness < best_fitness:
            best_positions, best_fitness = candidate, candidate_fitness
    return best_positions.reshape(-1, 2), -best_fitness

def run_dls_ii(objective_function, bounds, power_columns, data, max_iter=100):
    def dls_ii_objective_function(positions_flat):
        return objective_function(positions_flat, power_columns, data)
    best_positions = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    best_fitness = dls_ii_objective_function(best_positions)
    step_size = 10
    for _ in range(max_iter):
        candidate = best_positions + np.random.normal(0, step_size, size=best_positions.shape)
        candidate = np.clip(candidate, [b[0] for b in bounds], [b[1] for b in bounds])
        candidate_fitness = dls_ii_objective_function(candidate)
        if candidate_fitness < best_fitness:
            best_positions, best_fitness = candidate, candidate_fitness
        step_size *= 0.9
    return best_positions.reshape(-1, 2), -best_fitness

all_results = []

for file_path, dataset_name in files.items():
    data = pd.read_csv(f"dataset/{file_path}")
    power_columns = [col for col in data.columns if 'Power' in col]
    bounds = [(0, 1000) for _ in range(len(power_columns) * 2)]
    
    best_positions_de, best_power_de = run_de(objective_function, bounds, power_columns, data)
    best_positions_ide, best_power_ide = run_ide(objective_function, bounds, power_columns, data)
    best_positions_ls_nm, best_power_ls_nm = run_ls_nm(objective_function, bounds, power_columns, data)
    best_positions_dls_i, best_power_dls_i = run_dls_i(objective_function, bounds, power_columns, data)
    best_positions_dls_ii, best_power_dls_ii = run_dls_ii(objective_function, bounds, power_columns, data)
    
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "DE",
        "Best Layout": best_positions_de.tolist(),
        "Maximized Power": best_power_de
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "IDE",
        "Best Layout": best_positions_ide.tolist(),
        "Maximized Power": best_power_ide
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "LS-NM",
        "Best Layout": best_positions_ls_nm.tolist(),
        "Maximized Power": best_power_ls_nm
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "DLS(I)",
        "Best Layout": best_positions_dls_i.tolist(),
        "Maximized Power": best_power_dls_i
    })
    all_results.append({
        "Dataset": dataset_name,
        "Algorithm": "DLS(II)",
        "Best Layout": best_positions_dls_ii.tolist(),
        "Maximized Power": best_power_dls_ii
    })

with open('results_advanced_combined.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Dataset", "Algorithm", "Best Layout", "Maximized Power"])
    writer.writeheader()
    writer.writerows(all_results)

print("All results saved to 'results_advanced_combined.csv'")
