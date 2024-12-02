
import numpy as np
from scipy.optimize import differential_evolution, minimize
from geneticalgorithm import geneticalgorithm as ga
from pyswarm import pso
from cma import CMAEvolutionStrategy

# Function to calculate the power output of the wave farm
def power_output(position, wave_model, farm_size, constraints):
    power = -np.sum(np.sqrt((position ** 2)))
    return power

# Constraint function
def constraint_function(position, min_distance):
    for i in range(0, len(position), 2):
        for j in range(i + 2, len(position), 2):
            dist = np.sqrt((position[i] - position[j]) ** 2 + (position[i+1] - position[j+1]) ** 2)
            if dist < min_distance:
                return False
    return True

# General configuration
wave_model = "Perth"
farm_size = (1000, 1000)
min_distance = 50
num_buoys = 49
bounds = [(0, farm_size[0])] * num_buoys + [(0, farm_size[1])] * num_buoys

# Algorithms
def run_de():
    result = differential_evolution(
        power_output, bounds,
        args=(wave_model, farm_size, constraint_function),
        strategy='best1bin', maxiter=1000, popsize=15
    )
    return result

def run_ide():
    result = differential_evolution(
        power_output, bounds,
        args=(wave_model, farm_size, constraint_function),
        strategy='randtobest1bin', mutation=(0.5, 1.5), maxiter=1000, popsize=20
    )
    return result

def run_ls_nm():
    result = minimize(
        power_output, np.random.uniform(0, farm_size[0], num_buoys * 2),
        args=(wave_model, farm_size, constraint_function),
        method='Nelder-Mead'
    )
    return result

def run_dls_i():
    initial_positions = np.random.uniform(0, farm_size[0], num_buoys * 2)
    positions = initial_positions.copy()
    step_size = 50
    for _ in range(100):
        perturbation = np.random.uniform(-step_size, step_size, num_buoys * 2)
        candidate_positions = positions + perturbation
        if constraint_function(candidate_positions, min_distance):
            positions = candidate_positions
    return positions

def run_dls_ii():
    initial_positions = np.random.uniform(0, farm_size[0], num_buoys * 2)
    positions = initial_positions.copy()
    step_size = 50
    for _ in range(100):
        perturbation = np.random.normal(0, step_size, num_buoys * 2)
        candidate_positions = positions + perturbation
        if constraint_function(candidate_positions, min_distance):
            positions = candidate_positions
    return positions

def run_cmaes():
    cma = CMAEvolutionStrategy(np.random.uniform(0, farm_size[0], num_buoys * 2), 0.5)
    while not cma.stop():
        solutions = cma.ask()
        cma.tell(solutions, [power_output(sol, wave_model, farm_size, constraint_function) for sol in solutions])
    return cma.result

def run_2plus2_cmaes():
    cma = CMAEvolutionStrategy(np.random.uniform(0, farm_size[0], num_buoys * 2), 0.3, {'popsize': 2})
    while not cma.stop():
        solutions = cma.ask()
        cma.tell(solutions, [power_output(sol, wave_model, farm_size, constraint_function) for sol in solutions])
    return cma.result

def run_bga():
    # تعریف تابع هدف با آرگومان‌های ثابت برای الگوریتم ژنتیک
    def objective_function(position):
        return power_output(position, wave_model, farm_size, constraint_function)
    
    model = ga(
        function=objective_function,  # تابع هدف اصلاح شده
        dimension=num_buoys * 2,
        variable_type='bool',
        variable_boundaries=bounds
    )
    model.run()
    return model.output_dict


def run_bde():
    result = differential_evolution(
        power_output, bounds,
        args=(wave_model, farm_size, constraint_function),
        strategy='rand1bin', mutation=(0.4, 1.2), maxiter=500, popsize=10
    )
    return result

def run_bps():
    lb = [0] * len(bounds)
    ub = [1] * len(bounds)
    result = pso(
        power_output, lb, ub,
        args=(wave_model, farm_size, constraint_function),
        swarmsize=30, maxiter=100
    )
    return result

def run_1plus1_ea():
    position = np.random.uniform(0, farm_size[0], num_buoys * 2)
    for _ in range(1000):
        candidate = position + np.random.normal(0, 50, len(position))
        if constraint_function(candidate, min_distance) and power_output(candidate, wave_model, farm_size, constraint_function) > power_output(position, wave_model, farm_size, constraint_function):
            position = candidate
    return position

# Execute all algorithms
results = {
    "DE": run_de(),
    "IDE": run_ide(),
    "LS-NM": run_ls_nm(),
    "DLS(I)": run_dls_i(),
    "DLS(II)": run_dls_ii(),
    "CMAES": run_cmaes(),
    "2+2 CMAES": run_2plus2_cmaes(),
    "bGA": run_bga(),
    "bDE": run_bde(),
    "bPSO": run_bps(),
    "1+1 EA": run_1plus1_ea()
}

for algo, result in results.items():
    print(f"{algo} Result: {result}")
