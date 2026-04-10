import numpy as np
import math as m

def transformation_relative_to_pivot(transformation_matrix: np.array, pivot: np.array) -> np.array:
    a, b = pivot
    translate_to_origin = np.array(
        [
            [1.0, 0.0, -a],
            [0.0, 1.0, -b],
            [0.0, 0.0, 1.0],
        ]
    )

    translate_back = np.array(
        [
            [1.0, 0.0, a],
            [0.0, 1.0, b],
            [0.0, 0.0, 1.0],
        ]
    )

    return translate_back @ transformation_matrix @ translate_to_origin

def get_translation_matrix(t_x: float, t_y: float) -> np.ndarray:
    return np.array([
            [1.0, 0.0, t_x],
            [0.0, 1.0, t_y],
            [0.0, 0.0, 1.0],
    ])

def get_scale_matrix(s_x: float, s_y: float) -> np.ndarray:
    return np.array([
            [s_x, 0.0, 0.0],
            [0.0, s_y, 0.0],
            [0.0, 0.0, 1.0],
    ])

def get_rotation_matrix(phi_degrees: float) -> np.ndarray:
    cos_ = np.cos(np.deg2rad(phi_degrees))
    sin_ = np.sin(np.deg2rad(phi_degrees))
    return np.array([
            [cos_, -sin_, 0.0],
            [sin_, cos_, 0.0],
            [0.0, 0.0, 1.0],
    ])

def apply_transformation_matrix(transformation_matrix: np.ndarray, homogeneous_points: np.ndarray) -> list[np.ndarray]:
    return [(transformation_matrix @ point.reshape(3, 1)).flatten() for point in homogeneous_points]

def homogeneous2standard(homogeneous_points: list[np.ndarray]) -> list[np.ndarray]:
    return [point[:2] for point in homogeneous_points]

def TRS_decomposition(TRS: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t_x, t_y = TRS[0, 2], TRS[1, 2]
    translation = get_translation_matrix(t_x, t_y)
    s_x, s_y = m.sqrt(TRS[0, 0] ** 2 + TRS[1, 0] ** 2), m.sqrt(TRS[0, 1] ** 2 + TRS[1, 1] ** 2)
    scale = get_scale_matrix(s_x, s_y)
    rotation = np.array([
        [TRS[0, 0] / s_x, TRS[0, 1] / s_x, 0.0],
        [TRS[1, 0] / s_y, TRS[1, 1] / s_y], 0.0,
        [0.0, 0.0, 1.0]
    ])
    phi = m.atan2(TRS[0,1], TRS[1,1])
    return translation, scale, rotation

def inverse_translation_matrix(translation_matrix: np.ndarray) -> np.ndarray:
    t_x = translation_matrix[0, 2]
    t_y = translation_matrix[1, 2]
    return np.array([
        [1.0, 0.0, -t_x],
        [0.0, 1.0, -t_y],
        [0.0, 0.0, 1.0],
    ])


def inverse_scale_matrix(scale_matrix: np.ndarray) -> np.ndarray:
    s_x = scale_matrix[0, 0]
    s_y = scale_matrix[1, 1]

    if s_x == 0 or s_y == 0:
        raise ValueError("Scale matrix is not invertible because one of scale factors is zero.")

    return np.array([
        [1.0 / s_x, 0.0, 0.0],
        [0.0, 1.0 / s_y, 0.0],
        [0.0, 0.0, 1.0],
    ])


def inverse_rotation_matrix(rotation_matrix: np.ndarray) -> np.ndarray:
    return rotation_matrix.T


def inverse_transformation_relative_to_pivot(transformation_matrix: np.ndarray, pivot: np.ndarray) -> np.ndarray:
    a, b = pivot

    translate_to_origin = np.array([
        [1.0, 0.0, -a],
        [0.0, 1.0, -b],
        [0.0, 0.0, 1.0],
    ])

    translate_back = np.array([
        [1.0, 0.0, a],
        [0.0, 1.0, b],
        [0.0, 0.0, 1.0],
    ])

    inverse_transformation = np.linalg.inv(transformation_matrix)

    return translate_back @ inverse_transformation @ translate_to_origin


def inverse_affine_matrix(matrix: np.ndarray) -> np.ndarray:
    return np.linalg.inv(matrix)