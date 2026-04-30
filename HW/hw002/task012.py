import utils002 as utils
import numpy as np


def decompose_TRS_3d(TRS):
    t = TRS[0:3, 3]
    T = utils.get_translation_matrix(t[0], t[1], t[2])
    s_x = np.sqrt(TRS[0, 0] ** 2 + TRS[1, 0] ** 2 + TRS[2, 0] ** 2)
    s_y = np.sqrt(TRS[0, 1] ** 2 + TRS[1, 1] ** 2 + TRS[2, 1] ** 2)
    s_z = np.sqrt(TRS[0, 2] ** 2 + TRS[1, 2] ** 2 + TRS[2, 2] ** 2)
    S = utils.get_scale_matrix(s_x, s_y, s_z)
    R = np.array([
        [TRS[0, 0] / s_x, TRS[0, 1] / s_y, TRS[0, 2] / s_z, 0.0],
        [TRS[1, 0] / s_x, TRS[1, 1] / s_y, TRS[1, 2] / s_z, 0.0],
        [TRS[2, 0] / s_x, TRS[2, 1] / s_y, TRS[2, 2] / s_z, 0.0],
        [0.0,              0.0,              0.0,              1.0],
    ])
    return T, R, S

def is_orthogonal(matrix):
    R = matrix[:3, :3]
    I = np.eye(3)
    return np.allclose(R @ R.T, I)

def decompose_R(R: np.ndarray[float]):
    R = R[:3, :3]
    theta = np.arccos((np.trace(R) - 1 ) / 2)
    rotation_axis = np.array([
        R[2, 1] - R[1, 2],
        R[0, 2] - R[2, 0],
        R[1, 0] - R[0, 1],
    ])
    return theta, rotation_axis


if __name__ == '__main__':
    TRS = np.array([
        [2 * np.cos(np.deg2rad(45)), -3 * np.sin(np.deg2rad(45)), 0.0, 5.0],
        [2 * np.sin(np.deg2rad(45)), 3 * np.cos(np.deg2rad(45)), 0.0, -2.0],
        [0.0, 0.0, 4.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
    ])
    T, R, S = decompose_TRS_3d(TRS)
    utils.print_matrix("Translation = ",T)
    utils.print_matrix("Rotation = ",R)
    utils.print_matrix("Scale = ",S)
    if is_orthogonal(R):
        print("R is orthogonal")
        theta, rotation_axis = decompose_R(R)
        print(f"theta = {theta} rad")
        print(f"rotation_axis = {rotation_axis}")
    else:
        print("R is not orthogonal")
