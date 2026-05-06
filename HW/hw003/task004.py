import numpy as np
from matplotlib import pyplot as plt

import utils003 as utils


if __name__ == "__main__":
    delta_deg = 30.0
    alpha_values = np.linspace(-180.0, 180.0, 361)
    gamma_values = alpha_values - delta_deg

    print("For beta = 90 deg in external XYZ convention the matrix depends only on (alpha - gamma).")
    print(f"Example invariant value: alpha - gamma = {delta_deg} deg")
    print()

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(alpha_values, gamma_values, color="darkorange", linewidth=2.0)
    ax.scatter([30, 60, 120], [0, 30, 90], color="navy", s=45)
    ax.set_title("Gimbal Lock at beta = 90 deg")
    ax.set_xlabel("alpha (deg)")
    ax.set_ylabel("gamma (deg)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.text(
        -165,
        145,
        r"$\gamma = \alpha - \Delta,\ \Delta = 30^\circ$",
        fontsize=11,
        color="darkred",
    )

    output_path = utils.get_task_output_path(1)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
