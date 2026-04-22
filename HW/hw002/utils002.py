import inspect

import numpy as np
import math as m
import os.path

from src.engine.scene.Scene import Scene
from src.engine.model.Polygon import Polygon
from src.engine.model.Point import SimplePoint
from src.engine.model.LineModel import LineModel


def transformation_relative_to_pivot(transformation_matrix: np.ndarray, pivot: np.ndarray) -> np.ndarray:
    a, b, c = pivot
    translate_to_origin = np.array(
        [
            [1.0, 0.0, 0.0, -a],
            [0.0, 1.0, 0.0, -b],
            [0.0, 0.0, 1.0, -c],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    translate_back = np.array(
        [
            [1.0, 0.0, 0.0, a],
            [0.0, 1.0, 0.0, b],
            [0.0, 0.0, 1.0, c],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    return translate_back @ transformation_matrix @ translate_to_origin


def get_translation_matrix(t_x: float, t_y: float, t_z: float) -> np.ndarray:
    return np.array([
        [1.0, 0.0, 0.0, t_x],
        [0.0, 1.0, 0.0, t_y],
        [0.0, 0.0, 1.0, t_z],
        [0.0, 0.0, 0.0, 1.0],
    ])


def get_scale_matrix(s_x: float, s_y: float, s_z: float) -> np.ndarray:
    return np.array([
        [s_x, 0.0, 0.0, 0.0],
        [0.0, s_y, 0.0, 0.0],
        [0.0, 0.0, s_z, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])


def get_rotation_matrix_x(phi_degrees: float) -> np.ndarray:
    cos_ = np.cos(np.deg2rad(phi_degrees))
    sin_ = np.sin(np.deg2rad(phi_degrees))
    return np.array([
        [1.0, 0.0,  0.0,   0.0],
        [0.0, cos_, -sin_, 0.0],
        [0.0, sin_, cos_,  0.0],
        [0.0, 0.0,  0.0,   1.0],
    ])


def get_rotation_matrix_y(phi_degrees: float) -> np.ndarray:
    cos_ = np.cos(np.deg2rad(phi_degrees))
    sin_ = np.sin(np.deg2rad(phi_degrees))
    return np.array([
        [cos_,  0.0, sin_, 0.0],
        [0.0,   1.0, 0.0,  0.0],
        [-sin_, 0.0, cos_, 0.0],
        [0.0,   0.0, 0.0,  1.0],
    ])


def get_rotation_matrix_z(phi_degrees: float) -> np.ndarray:
    cos_ = np.cos(np.deg2rad(phi_degrees))
    sin_ = np.sin(np.deg2rad(phi_degrees))
    return np.array([
        [cos_, -sin_, 0.0, 0.0],
        [sin_, cos_,  0.0, 0.0],
        [0.0,  0.0,   1.0, 0.0],
        [0.0,  0.0,   0.0, 1.0],
    ])

def get_rotation_matrix(phi_degrees: float, axis: np.ndarray) -> np.ndarray:
    axis = np.array(axis, dtype=float)

    if axis.shape != (3,):
        raise ValueError("axis must be a 3D vector")

    norm = np.linalg.norm(axis)
    if np.isclose(norm, 0.0):
        raise ValueError("axis vector must be non-zero")

    x, y, z = axis / norm

    phi = np.deg2rad(phi_degrees)
    cos_ = np.cos(phi)
    sin_ = np.sin(phi)
    one_minus_cos = 1.0 - cos_

    return np.array([
        [
            cos_ + x * x * one_minus_cos,
            x * y * one_minus_cos - z * sin_,
            x * z * one_minus_cos + y * sin_,
            0.0,
        ],
        [
            y * x * one_minus_cos + z * sin_,
            cos_ + y * y * one_minus_cos,
            y * z * one_minus_cos - x * sin_,
            0.0,
        ],
        [
            z * x * one_minus_cos - y * sin_,
            z * y * one_minus_cos + x * sin_,
            cos_ + z * z * one_minus_cos,
            0.0,
        ],
        [0.0, 0.0, 0.0, 1.0],
    ])

def get_rotation_matrix_euler(
    angles_degrees: np.ndarray | list[float] | tuple[float, float, float],
    order: str = "XYZ",
) -> np.ndarray:
    if len(angles_degrees) != 3:
        raise ValueError("angles_degrees must contain exactly 3 angles")

    order = order.upper()
    if len(order) != 3 or any(axis not in "XYZ" for axis in order):
        raise ValueError("order must be a 3-character string using only X, Y, Z")

    def get_rotation_matrix(phi_degrees: float, axis: str) -> np.ndarray:
        phi = np.deg2rad(phi_degrees)
        cos_ = np.cos(phi)
        sin_ = np.sin(phi)

        if axis == "X":
            return np.array([
                [1.0, 0.0,  0.0,   0.0],
                [0.0, cos_, -sin_, 0.0],
                [0.0, sin_, cos_,  0.0],
                [0.0, 0.0,  0.0,   1.0],
            ])

        if axis == "Y":
            return np.array([
                [cos_,  0.0, sin_, 0.0],
                [0.0,   1.0, 0.0,  0.0],
                [-sin_, 0.0, cos_, 0.0],
                [0.0,   0.0, 0.0,  1.0],
            ])

        if axis == "Z":
            return np.array([
                [cos_, -sin_, 0.0, 0.0],
                [sin_, cos_,  0.0, 0.0],
                [0.0,  0.0,   1.0, 0.0],
                [0.0,  0.0,   0.0, 1.0],
            ])

        raise ValueError("axis must be one of: 'X', 'Y', 'Z'")

    result = np.eye(4)

    for phi_degrees, axis in zip(angles_degrees, order):
        result = result @ get_rotation_matrix(phi_degrees, axis)

    return result


def apply_transformation_matrix(transformation_matrix: np.ndarray, homogeneous_points: np.ndarray) -> list[np.ndarray]:
    return [(transformation_matrix @ point.reshape(4, 1)).flatten() for point in homogeneous_points]


def homogeneous2standard(homogeneous_points: list[np.ndarray]) -> list[np.ndarray]:
    return [point[:3] for point in homogeneous_points]


def standard2homogeneous(standard_objects, kind: str = "point") -> np.ndarray:
    if kind not in ("point", "vector"):
        raise ValueError("kind must be either 'point' or 'vector'")

    last_coordinate = 1.0 if kind == "point" else 0.0

    return np.array([
        np.array([obj[0], obj[1], obj[2], last_coordinate], dtype=float)
        for obj in standard_objects
    ])


def is_rotation_matrix(R: np.ndarray, eps: float = 1e-6) -> bool:
    if R.shape == (4, 4):
        R3 = R[:3, :3]
    else:
        R3 = R

    RtR = R3.T @ R3
    I = np.eye(R3.shape[0])
    return np.allclose(RtR, I, atol=eps) and np.isclose(np.linalg.det(R3), 1.0, atol=eps)


def decompose_TRS(TRS: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t_x, t_y, t_z = TRS[0, 3], TRS[1, 3], TRS[2, 3]
    translation = get_translation_matrix(t_x, t_y, t_z)

    s_x = m.sqrt(TRS[0, 0] ** 2 + TRS[1, 0] ** 2 + TRS[2, 0] ** 2)
    s_y = m.sqrt(TRS[0, 1] ** 2 + TRS[1, 1] ** 2 + TRS[2, 1] ** 2)
    s_z = m.sqrt(TRS[0, 2] ** 2 + TRS[1, 2] ** 2 + TRS[2, 2] ** 2)

    scale = get_scale_matrix(s_x, s_y, s_z)

    rotation = np.array([
        [TRS[0, 0] / s_x, TRS[0, 1] / s_y, TRS[0, 2] / s_z, 0.0],
        [TRS[1, 0] / s_x, TRS[1, 1] / s_y, TRS[1, 2] / s_z, 0.0],
        [TRS[2, 0] / s_x, TRS[2, 1] / s_y, TRS[2, 2] / s_z, 0.0],
        [0.0,             0.0,             0.0,             1.0],
    ])

    if not is_rotation_matrix(rotation):
        raise ValueError("This matrix cannot be decomposed into pure T, R, S with diagonal scale.")

    return translation, rotation, scale


def inverse_translation_matrix(translation_matrix: np.ndarray) -> np.ndarray:
    t_x = translation_matrix[0, 3]
    t_y = translation_matrix[1, 3]
    t_z = translation_matrix[2, 3]
    return np.array([
        [1.0, 0.0, 0.0, -t_x],
        [0.0, 1.0, 0.0, -t_y],
        [0.0, 0.0, 1.0, -t_z],
        [0.0, 0.0, 0.0, 1.0],
    ])


def inverse_scale_matrix(scale_matrix: np.ndarray) -> np.ndarray:
    s_x = scale_matrix[0, 0]
    s_y = scale_matrix[1, 1]
    s_z = scale_matrix[2, 2]

    if s_x == 0 or s_y == 0 or s_z == 0:
        raise ValueError("Scale matrix is not invertible because one of scale factors is zero.")

    return np.array([
        [1.0 / s_x, 0.0,       0.0,       0.0],
        [0.0,       1.0 / s_y, 0.0,       0.0],
        [0.0,       0.0,       1.0 / s_z, 0.0],
        [0.0,       0.0,       0.0,       1.0],
    ])


def inverse_rotation_matrix(rotation_matrix: np.ndarray) -> np.ndarray:
    R = rotation_matrix[:3, :3].T
    result = np.eye(4)
    result[:3, :3] = R
    return result


def inverse_transformation_relative_to_pivot(transformation_matrix: np.ndarray, pivot: np.ndarray) -> np.ndarray:
    a, b, c = pivot

    translate_to_origin = np.array([
        [1.0, 0.0, 0.0, -a],
        [0.0, 1.0, 0.0, -b],
        [0.0, 0.0, 1.0, -c],
        [0.0, 0.0, 0.0, 1.0],
    ])

    translate_back = np.array([
        [1.0, 0.0, 0.0, a],
        [0.0, 1.0, 0.0, b],
        [0.0, 0.0, 1.0, c],
        [0.0, 0.0, 0.0, 1.0],
    ])

    inverse_transformation = np.linalg.inv(transformation_matrix)

    return translate_back @ inverse_transformation @ translate_to_origin


def inverse_affine_matrix(matrix: np.ndarray) -> np.ndarray:
    return np.linalg.inv(matrix)


def print_matrix(name: str, matrix: np.ndarray, precision: int = 3) -> None:
    print(f"{name} =")
    print(np.array2string(matrix, precision=precision, suppress_small=True))
    print()


def print_matrices(
    matrices,
    precision: int = 3,
    names: list[str] | None = None,
) -> None:
    if isinstance(matrices, np.ndarray):
        matrices = [matrices]

    if names is not None and len(names) != len(matrices):
        raise ValueError("names and matrices must have the same length")

    for i, matrix in enumerate(matrices):
        name = names[i] if names is not None else f"M{i + 1}"
        print_matrix(name, matrix, precision)