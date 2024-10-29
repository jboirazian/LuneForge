import numpy as np
from scipy.optimize import fsolve


def get_effective_permitivity(f1:float,f2:float,epsilon1:float,epsilon2:float):
    # Bruggeman equation to solve for epsilon_eff
    def bruggeman_eq(epsilon_eff:float):
        term1 = f1 * (epsilon1 - epsilon_eff) / (epsilon1 + 2 * epsilon_eff)
        term2 = f2 * (epsilon2 - epsilon_eff) / (epsilon2 + 2 * epsilon_eff)
        return term1 + term2

    # Initial guess for epsilon_eff
    epsilon_eff_initial_guess = (epsilon1 * f1 + epsilon2 * f2)

    # Solving the equation using fsolve
    epsilon_eff_solution = fsolve(bruggeman_eq, epsilon_eff_initial_guess)

    return epsilon_eff_solution