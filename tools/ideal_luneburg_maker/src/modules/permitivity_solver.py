import numpy as np
from scipy.optimize import fsolve


# Calculate f2 given an effective permittivity, epsilon1, and epsilon2
def calculate_f2(epsilon_eff, epsilon1, epsilon2):
    def bruggeman_eq(f2):
        f1 = 1 - f2
        term1 = f1 * (epsilon1 - epsilon_eff) / (epsilon1 + 2 * epsilon_eff)
        term2 = f2 * (epsilon2 - epsilon_eff) / (epsilon2 + 2 * epsilon_eff)
        return term1 + term2

    # Initial guess for f2
    f2_initial_guess = 0.5
    f2_solution = fsolve(bruggeman_eq, f2_initial_guess)[0]

    # Ensure f2 is within valid bounds
    if 0 <= f2_solution <= 1:
        f1_solution = 1 - f2_solution
        return f2_solution, f1_solution
    else:
        raise ValueError("No valid solution for f2 in the range [0, 1]")

# Luneburg equation for required permittivity at radius R
def luneburg_eq(Ro, R):
    return 2 - ((Ro ** 2) / (R ** 2))

def get_ratio(epsilon1:float,epsilon2:float,min_epsilon:float,sphere_radius:float,center_distance:float):
    epsilon_Ro = luneburg_eq(Ro=center_distance, R=sphere_radius)
    print(f"epsilon_Ro = {epsilon_Ro}")
    if min_epsilon > epsilon_Ro:
        epsilon_Ro = min_epsilon
    print(f"epsilon_Ro = {epsilon_Ro} | {epsilon1} {epsilon2}")
    f2, f1 = calculate_f2(epsilon_eff=epsilon_Ro, epsilon1=epsilon1, epsilon2=epsilon2)
    return f2,f1