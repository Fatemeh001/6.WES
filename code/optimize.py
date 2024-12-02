import pandas as pd
import numpy as np
import csv
from scipy.optimize import differential_evolution, minimize
from cma import CMAEvolutionStrategy
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

def run_cmaes(objective_function, bounds, power_columns, data, max_iter=100):
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

def run_cmaes_2plus2(objective_function, bounds, power_columns, data, max_iter=100):
    initial_point = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    sigma = 0.5
    es = CMAEvolutionStrategy(initial_point, sigma, {'popsize': 2})
    for _ in range(max_iter):
        solutions = es.ask()
        fitness = [objective_function(np.array(sol), power_columns, data) for sol in solutions]
        es.tell(solutions, fitness)
        if es.stop():
            break
    return es.result.xbest, -es.result.fbest

def run_bga(objective_function, bounds, power_columns, data, max_iter=100):
    n_dim = len(bounds)
    ga = GA(func=lambda x: objective_function(x, power_columns, data), n_dim=n_dim, size_pop=50, max_iter=max_iter, prob_mut=0.1)
    best_x, best_y = ga.run()
    return best_x.reshape(-1, 2), -best_y

def run_bde(objective_function, bounds, power_columns, data, max_iter=100):
    n_dim = len(bounds)
    de = DE(func=lambda x: objective_function(x, power_columns, data), n_dim=n_dim, size_pop=50, max_iter=max_iter)
    best_x, best_y = de.run()
    return best_x.reshape(-1, 2), -best_y

def run_bpso(objective_function, bounds, power_columns, data, max_iter=100):
    n_dim = len(bounds)
    pso = PSO(func=lambda x: objective_function(x, power_columns, data), n_dim=n_dim, pop=50, max_iter=max_iter)
    best_x, best_y = pso.run()
    return best_x.reshape(-1, 2), -best_y

def evolutionary_algorithm(objective_function, bounds, power_columns, data, max_iter=100):
    x = np.random.uniform([b[0] for b in bounds], [b[1] for b in bounds])
    fx = objective_function(x, power_columns, data)
    for _ in range(max_iter):
        candidate = x + np.random.normal(0, 10, size=x.shape)
        candidate = np.clip(candidate, [b[0] for b in bounds], [b[1] for b in bounds])
        fcandidate = objective_function(candidate, power_columns, data)
        if fcandidate < fx:
            x, fx = candidate, fcandidate
    return x, -fx

all_results = []

for file_path, dataset_name in files.items():
    data = pd.read_csv(f"dataset/{file_path}")
    power_columns = [col for col in data.columns if 'Power' in col]
    bounds = [(0, 1000) for _ in range(len(power_columns) * 2)]
    
    algorithms = {
        "DE": run_de,
        "IDE": run_ide,
        "LS-NM": run_ls_nm,
        "DLS(I)": run_dls_i,
        "DLS(II)": run_dls_ii,
        "CMAES": run_cmaes,
        "2+2 CMAES": run_cmaes_2plus2,
        "bGA": run_bga,
        "bDE": run_bde,
        "bPSO": run_bpso,
        "1+1 EA": evolutionary_algorithm
    }
    
    for algo_name, algo_func in algorithms.items():
        best_positions, best_power = algo_func(objective_function, bounds, power_columns, data)
        all_results.append({
            "Dataset": dataset_name,
            "Algorithm": algo_name,
            "Best Layout": best_positions.tolist(),
            "Maximized Power": best_power
        })

with open('combined_results_all_algorithms.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Dataset", "Algorithm", "Best Layout", "Maximized Power"])
    writer.writeheader()
    writer.writerows(all_results)

print("All results saved to 'combined_results_all_algorithms.csv'")
