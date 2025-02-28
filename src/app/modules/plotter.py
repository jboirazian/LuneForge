import matplotlib.pyplot as plt


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