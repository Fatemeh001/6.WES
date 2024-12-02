import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution, minimize
from geneticalgorithm import geneticalgorithm as ga
from pyswarm import pso
from cma import CMAEvolutionStrategy
import time
import xlsxwriter

# Dataset Information
datasets = {
    "Perth_49": "dataset/WEC_Perth_49.csv",
    "Perth_100": "dataset/WEC_Perth_100.csv",
    "Sydney_49": "dataset/WEC_Sydney_49.csv",
    "Sydney_100": "dataset/WEC_Sydney_100.csv"
}

farm_size = (100, 100)  # Farm dimensions
min_distance = 20  # Minimum distance between WECs

# Power output function
def power_output(position, data, num_wec, farm_size):
    total_power = 0
    for i in range(num_wec):
        x = position[2 * i]
        y = position[2 * i + 1]
        if not (0 <= x <= farm_size[0] and 0 <= y <= farm_size[1]):
            return float('inf')  # Penalty for invalid positions
        distances = np.sqrt((data[f'X{i+1}'] - x)**2 + (data[f'Y{i+1}'] - y)**2)
        closest_idx = np.argmin(distances)
        total_power += data[f'Power{i+1}'].iloc[closest_idx]
    return -total_power  # Negative for minimization

# Algorithm definitions
def run_de(data, bounds, num_wec):
    print("Starting DE...")
    start_time = time.time()
    result = differential_evolution(
        lambda pos: power_output(pos, data, num_wec, farm_size), bounds,
        maxiter=10, popsize=5, disp=True)
    print("DE finished in", time.time() - start_time, "seconds")
    return result.fun

def run_ide(data, bounds, num_wec):
    print("Starting IDE...")
    start_time = time.time()
    result = differential_evolution(
        lambda pos: power_output(pos, data, num_wec, farm_size), bounds,
        strategy='randtobest1bin', mutation=(0.5, 1.5), maxiter=10, popsize=5, disp=True)
    print("IDE finished in", time.time() - start_time, "seconds")
    return result.fun

def run_ls_nm(data, bounds, num_wec):
    print("Starting LS-NM...")
    start_time = time.time()
    result = minimize(
        lambda pos: power_output(pos, data, num_wec, farm_size),
        np.random.uniform(0, farm_size[0], len(bounds)), method='Nelder-Mead')
    print("LS-NM finished in", time.time() - start_time, "seconds")
    return result.fun

def run_dls_i(data, bounds, num_wec):
    print("Starting DLS(I)...")
    start_time = time.time()
    position = np.random.uniform(0, farm_size[0], len(bounds))
    step_size = 50
    for _ in range(10):
        candidate = position + np.random.uniform(-step_size, step_size, len(bounds))
        if power_output(candidate, data, num_wec, farm_size) < power_output(position, data, num_wec, farm_size):
            position = candidate
    print("DLS(I) finished in", time.time() - start_time, "seconds")
    return power_output(position, data, num_wec, farm_size)

def run_dls_ii(data, bounds, num_wec):
    print("Starting DLS(II)...")
    start_time = time.time()
    position = np.random.uniform(0, farm_size[0], len(bounds))
    step_size = 50
    for _ in range(10):
        candidate = position + np.random.normal(0, step_size, len(bounds))
        if power_output(candidate, data, num_wec, farm_size) < power_output(position, data, num_wec, farm_size):
            position = candidate
    print("DLS(II) finished in", time.time() - start_time, "seconds")
    return power_output(position, data, num_wec, farm_size)

def run_cmaes(data, bounds, num_wec):
    print("Starting CMAES...")
    start_time = time.time()
    cma = CMAEvolutionStrategy(np.random.uniform(0, farm_size[0], len(bounds)), 0.5)
    while not cma.stop():
        solutions = cma.ask()
        cma.tell(solutions, [power_output(sol, data, num_wec, farm_size) for sol in solutions])
    print("CMAES finished in", time.time() - start_time, "seconds")
    return cma.result[1]

def run_2plus2_cmaes(data, bounds, num_wec):
    print("Starting 2+2 CMAES...")
    start_time = time.time()
    cma = CMAEvolutionStrategy(np.random.uniform(0, farm_size[0], len(bounds)), 0.3, {'popsize': 2})
    while not cma.stop():
        solutions = cma.ask()
        cma.tell(solutions, [power_output(sol, data, num_wec, farm_size) for sol in solutions])
    print("2+2 CMAES finished in", time.time() - start_time, "seconds")
    return cma.result[1]

# def run_bga(data, bounds, num_wec):
#     print("Starting bGA...")
#     start_time = time.time()
#     def objective_function(pos):
#         return power_output(pos, data, num_wec, farm_size)
#     model = ga(function=objective_function, dimension=len(bounds), variable_type='bool', variable_boundaries=bounds)
#     model.run()
#     print("bGA finished in", time.time() - start_time, "seconds")
#     return model.output_dict['function']

# def run_bps(data, bounds, num_wec):
#     print("Starting bPSO...")
#     start_time = time.time()
#     lb = [0] * len(bounds)
#     ub = [farm_size[0]] * len(bounds)
#     result = pso(lambda pos: power_output(pos, data, num_wec, farm_size), lb, ub, swarmsize=3, maxiter=10)
#     print("bPSO finished in", time.time() - start_time, "seconds")
#     return result[1]

def run_1plus1_ea(data, bounds, num_wec):
    print("Starting 1+1 EA...")
    start_time = time.time()
    position = np.random.uniform(0, farm_size[0], len(bounds))
    for _ in range(10):
        candidate = position + np.random.normal(0, 50, len(bounds))
        if power_output(candidate, data, num_wec, farm_size) < power_output(position, data, num_wec, farm_size):
            position = candidate
    print("1+1 EA finished in", time.time() - start_time, "seconds")
    return power_output(position, data, num_wec, farm_size)

# Run algorithms on each dataset
results = []
for name, path in datasets.items():
    dataset_start_time = time.time()
    print(f"Processing dataset: {name}")
    data = pd.read_csv(path)
    num_wec = 49 if "49" in name else 100
    bounds = [(0, farm_size[0])] * num_wec * 2

    dataset_results = {
        "Dataset": name,
        "DE": run_de(data, bounds, num_wec),
        "IDE": run_ide(data, bounds, num_wec),
        "LS-NM": run_ls_nm(data, bounds, num_wec),
        "DLS(I)": run_dls_i(data, bounds, num_wec),
        "DLS(II)": run_dls_ii(data, bounds, num_wec),
        "CMAES": run_cmaes(data, bounds, num_wec),
        "2+2 CMAES": run_2plus2_cmaes(data, bounds, num_wec),
        # "bGA": run_bga(data, bounds, num_wec),
        # "bPSO": run_bps(data, bounds, num_wec),
        "1+1 EA": run_1plus1_ea(data, bounds, num_wec)
    }
    results.append(dataset_results)
    print(f"Finished {name} in {time.time() - dataset_start_time:.2f} seconds")

    # Save intermediate results
    pd.DataFrame(results).to_excel("partial_results.xlsx", index=False)
    print(f"Partial results saved for {name}")



# Save final results
results_df = pd.DataFrame(results)
results_df.to_excel("optimization_results.xlsx", index=False)
print("Final results saved in optimization_results.xlsx")
