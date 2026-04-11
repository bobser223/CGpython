import inspect

import numpy as np
import math as m
import os.path

from src.engine.scene.Scene import Scene
from src.engine.model.Polygon import Polygon
from src.engine.model.Point import SimplePoint
from src.engine.model.LineModel import LineModel


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

def standard2homogeneous(standard_objects,kind: str = "point",) -> np.array[np.ndarray]:
    if kind not in ("point", "vector"):
        raise ValueError("kind must be either 'point' or 'vector'")

    last_coordinate = 1.0 if kind == "point" else 0.0

    return np.array([
        np.array([obj[0], obj[1], last_coordinate], dtype=float)
        for obj in standard_objects
    ])

def is_rotation_matrix(R: np.ndarray, eps: float = 1e-6) -> bool:
    RtR = R.T @ R
    I = np.eye(R.shape[0])
    return np.allclose(RtR, I, atol=eps) and np.isclose(np.linalg.det(R), 1.0, atol=eps)

def decompose_TRS(TRS: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t_x, t_y = TRS[0, 2], TRS[1, 2]
    translation = get_translation_matrix(t_x, t_y)
    s_x, s_y = m.sqrt(TRS[0, 0] ** 2 + TRS[1, 0] ** 2), m.sqrt(TRS[0, 1] ** 2 + TRS[1, 1] ** 2)
    scale = get_scale_matrix(s_x, s_y)
    rotation = np.array([
        [TRS[0, 0] / s_x, TRS[0, 1] / s_y, 0.0],
        [TRS[1, 0] / s_x, TRS[1, 1] / s_y, 0.0],
        [0.0, 0.0, 1.0]
    ])

    if not is_rotation_matrix(rotation):
        raise ValueError("This matrix cannot be decomposed into pure T, R, S with diagonal scale.")

    # phi = m.atan2(TRS[0,1], TRS[1,1])
    return translation, rotation, scale

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

def draw_polygone_no_pivot(square, transformed_square, output_name, coordinate_rect_=(-5, -5, 5, 5)):
    output_name += ".png"

    scene = Scene(
        image_size=(7, 7),
        coordinate_rect=coordinate_rect_,
        title="Task 008",
        grid_show=True,
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    original_square = Polygon(
        square,
        color="gray",
        linewidth=2.0,
        line_style="--",
        vertices_show=True,
        vertex_color="gray",
    )

    scene["original_square"] = original_square



    final_square = Polygon(
        transformed_square,
        color="blue",
        linewidth=2.5,
        line_style="solid",
        vertices_show=True,
        vertex_color="blue",
    )

    scene["final_square"] = final_square

    scene.show(output_file=output_name)

def draw_polygone_with_pivot(square, transformed_square, pivot = [0, 0], output_name="", coordinate_rect_=(-5, -5, 5, 5)):
    output_name += ".png"

    scene = Scene(
        image_size=(7, 7),
        coordinate_rect=coordinate_rect_,
        title="Task 008",
        grid_show=True,
        base_axis_show=False,
        axis_show=True,
        axis_color=("red", "green"),
        axis_line_style="-.",
        keep_aspect_ratio=True,
    )

    original_square = Polygon(
        square,
        color="gray",
        linewidth=2.0,
        line_style="--",
        vertices_show=True,
        vertex_color="gray",
    )

    scene["original_square"] = original_square

    final_square = Polygon(
        transformed_square,
        color="blue",
        linewidth=2.5,
        line_style="solid",
        vertices_show=True,
        vertex_color="blue",
    )

    pivot_point = SimplePoint(
        pivot,
        color="red",
        vertex_size=80,
        labels=((f"pivot ({pivot[0]}, {pivot[1]})", (0.08, 0.08)),),
        label_color="red",
        label_fontsize=12,
    )

    scene["pivot"] = pivot_point

    scene["final_square"] = final_square

    scene.show(output_file=output_name)