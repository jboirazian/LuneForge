import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Parameters
D = 140e-3  # Sphere radius in meters
f1 = 0.1    # Volume fraction of material 1
f2 = 0.9    # Volume fraction of material 2
epsilon1 = 1.0  # Permittivity of material 1
epsilon2 = 2.0  # Permittivity of material 2
min_epsion_Ro = 1.1
axis_cell_resolution= 10 # The amout of cells that are on a single axis , must be a even number

def generate_plots(name: str, data: dict):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot permittivity vs Ro
    axs[0].plot(data["Ro_values"], data["permittivity_values"], marker='o', color='b', label="Permittivity")
    axs[0].set_xlabel("Ro (meters)")
    axs[0].set_ylabel("Permittivity (ε)")
    axs[0].set_title("Variation of Permittivity vs. Ro")
    axs[0].grid(True)
    axs[0].legend()

    # Plot material ratio vs Ro
    axs[1].plot(data["Ro_values"], data["f2_ratio"], marker='o', color='r', label="Material ratio")
    axs[1].set_xlabel("Ro (meters)")
    axs[1].set_ylabel("Material ratio")
    axs[1].set_title("Material Ratio vs. Ro")
    axs[1].grid(True)
    axs[1].legend()

    # Plot air ratio vs Ro
    axs[2].plot(data["Ro_values"], data["f1_ratio"], marker='o', color='g', label="Air ratio")
    axs[2].set_xlabel("Ro (meters)")
    axs[2].set_ylabel("Air ratio")
    axs[2].set_title("Air Permittivity Ratio vs. Ro")
    axs[2].grid(True)
    axs[2].legend()

    # Save the figure
    fig.savefig(f"{name}.png", format="png", dpi=300)
    plt.close(fig)  # Close the figure to free memory if not displaying it



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

# Lists to store Ro and permittivity values
Ro_values = []
permittivity_values = []
f2_ratio = []
f1_ratio = []


# Calculate permittivity and f2 for each Ro in range
for Ro in np.linspace(-D / 2, D / 2, axis_cell_resolution):
    epsilon_Ro = luneburg_eq(Ro=Ro, R=D / 2)
    if min_epsion_Ro > epsilon_Ro:
        epsilon_Ro = min_epsion_Ro
    f2, f1 = calculate_f2(epsilon_eff=epsilon_Ro, epsilon1=epsilon1, epsilon2=epsilon2)    
    # Store Ro and permittivity for plotting
    Ro_values.append(Ro)
    permittivity_values.append(epsilon_Ro)
    f2_ratio.append(f2)
    f1_ratio.append(f1)


data ={}
data["Ro_values"]=Ro_values
data["permittivity_values"]=permittivity_values
data["f2_ratio"]=f2_ratio
data["f1_ratio"]=f1_ratio

print(f"Estimated cells {axis_cell_resolution**3}")

generate_plots(name="example",data=data)

