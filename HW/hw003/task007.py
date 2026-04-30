import numpy as np
import utils003 as utils


def rotation_matrix_to_euler_xyz_external(R, eps=1e-8):


    R = np.asarray(R, dtype=float)

    # If homogeneous 4x4 matrix was passed, take only 3x3 rotation part
    if R.shape == (4, 4):
        R = R[:3, :3]

    if R.shape != (3, 3):
        raise ValueError("R must be 3x3 or 4x4 matrix")

    # R[2, 0] = -sin(beta)
    sin_beta = -R[2, 0]

    # Numerical safety
    sin_beta = np.clip(sin_beta, -1.0, 1.0)

    beta = np.arcsin(sin_beta)
    cos_beta = np.cos(beta)

    # Normal case
    if abs(cos_beta) > eps:
        alpha = np.arctan2(R[2, 1], R[2, 2])
        gamma = np.arctan2(R[1, 0], R[0, 0])

    # Gimbal lock case
    else:
        # Force alpha = 0 for stable solution
        alpha = 0.0

        # Case beta = +90 degrees
        if sin_beta > 0:
            # delta = alpha - gamma
            delta = np.arctan2(R[0, 1], R[0, 2])

            # alpha = 0 => -gamma = delta
            gamma = -delta

        # Case beta = -90 degrees
        else:
            # sigma = alpha + gamma
            sigma = np.arctan2(-R[0, 1], -R[0, 2])

            # alpha = 0 => gamma = sigma
            gamma = sigma

    return np.rad2deg([alpha, beta, gamma])

if __name__ == '__main__':
    cube = utils.get_cube_vertices()
    base_angles = [30, 90, 45]
    equivalent_angles = [[40, 90, 55], [100, 90, 115]]

    R_base = utils.get_rotation_matrix_euler(base_angles, "XYZ", "external")
    R_alt_1 = utils.get_rotation_matrix_euler(equivalent_angles[0], "XYZ", "external")
    R_alt_2 = utils.get_rotation_matrix_euler(equivalent_angles[1], "XYZ", "external")

    print(f"R_base == R_alt_1: {np.allclose(R_base, R_alt_1)}")
    print(f"R_base == R_alt_2: {np.allclose(R_base, R_alt_2)}")
    print()
    print("Stable Euler solution with alpha forced to 0 in gimbal lock:")
    print(rotation_matrix_to_euler_xyz_external(R_base))
    print()

    utils.save_task_multiple_visualization(
        objects=[
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "transformation_matrix": R_base,
                "color": "deepskyblue",
                "edge_color": "navy",
                "alpha": 0.16,
            },
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "transformation_matrix": R_alt_1,
                "color": "salmon",
                "edge_color": "darkred",
                "alpha": 0.10,
            },
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "transformation_matrix": R_alt_2,
                "color": "gold",
                "edge_color": "saddlebrown",
                "alpha": 0.08,
            },
        ],
        title="HW003 Task 007",
    )
