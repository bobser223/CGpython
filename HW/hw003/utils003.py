import inspect
import sys
from pathlib import Path

import numpy as np
import math as m
import os.path

os.environ.setdefault("GRAPHIC_ENGINE_MPL_BACKEND", "Agg")

ENGINE_ROOT = Path(__file__).resolve().parents[2] / "GraphicEngine2D"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.append(str(ENGINE_ROOT))

from src.base.broken_line import draw_broken_line
from src.base.poligon import draw_poly
from src.engine.model.Model import Model
from src.engine.scene.Scene import Scene
from src.math.Mat4x4 import Mat4x4


class MeshModel(Model):
    def __init__(
        self,
        vertices,
        faces,
        color: str = "grey",
        edge_color: str = "black",
        line_style: str = "-",
        line_width: float = 1.0,
        alpha: float = 0.15,
    ):
        vertices = np.asarray(vertices, dtype=float)
        super().__init__(*vertices)

        self.faces = [tuple(face) for face in faces]
        self.color = color
        self.edge_color = edge_color
        self.line_style = line_style
        self.line_width = line_width
        self.alpha = alpha

    def draw_model(self, plt_axis):
        transformed_geometry = self.transformed_geometry
        points = [vertex.xyz for vertex in transformed_geometry]

        for face in self.faces:
            face_points = [points[index] for index in face]
            draw_poly(
                plt_axis,
                face_points,
                alpha=self.alpha,
                edgecolor=self.edge_color,
                facecolor=self.color,
            )
            draw_broken_line(
                plt_axis,
                face_points + [face_points[0]],
                color=self.edge_color,
                linewidth=self.line_width,
                linestyle=self.line_style,
            )


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
        rotation_type: str = "internal"
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
    #internal XYZ:
    #R = Rx @ Ry @ Rz



    if  rotation_type == "internal":
        for phi_degrees, axis in zip(angles_degrees, order):
            result = result @ get_rotation_matrix(phi_degrees, axis)
    # external XYZ:
    # R = Rz @ Ry @ Rx
    elif rotation_type == "external":
        for phi_degrees, axis in zip(angles_degrees, order):
            result = get_rotation_matrix(phi_degrees, axis) @ result
    else:
        raise ValueError("rotation_type must be one of: 'internal', 'external'")

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

def compare_rotation_matrices(R1: np.ndarray, R2: np.ndarray, eps: float = 1e-6) -> bool:
    R1 = R1.reshape(4, 4)
    R2 = R2.reshape(4, 4)
    return np.allclose(R1, R2, atol=eps)


def get_cube_faces() -> list[tuple[int, ...]]:
    return [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (1, 2, 6, 5),
        (0, 3, 7, 4),
    ]


def get_tetrahedron_faces() -> list[tuple[int, ...]]:
    return [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
    ]


def infer_faces_from_vertices(vertices) -> list[tuple[int, ...]]:
    vertices = _normalize_points(vertices)
    points_count = len(vertices)

    if points_count == 3:
        return [(0, 1, 2)]
    if points_count == 4:
        return [(0, 1, 2, 3)]

    raise ValueError("faces must be provided for objects with more than 4 vertices")


def to_engine_matrix(matrix: np.ndarray) -> Mat4x4:
    return Mat4x4(np.asarray(matrix, dtype=float))


def _normalize_points(points) -> np.ndarray:
    array = np.asarray(points, dtype=float)

    if array.ndim == 1:
        array = array.reshape(1, -1)

    if array.ndim != 2 or array.shape[1] not in (3, 4):
        raise ValueError("points must be a 2D array with shape (n, 3) or (n, 4)")

    if array.shape[1] == 4:
        w = array[:, 3]
        result = array[:, :3].copy()
        point_mask = ~np.isclose(w, 0.0)
        if np.any(point_mask):
            result[point_mask] = result[point_mask] / w[point_mask, None]
        return result

    return array


def get_coordinate_rect(*point_sets, padding: float = 1.0) -> tuple[float, float, float, float, float, float]:
    normalized_sets = [_normalize_points(points) for points in point_sets if points is not None]
    if not normalized_sets:
        raise ValueError("at least one point set must be provided")

    all_points = np.vstack(normalized_sets)
    mins = all_points.min(axis=0)
    maxs = all_points.max(axis=0)

    spans = maxs - mins
    spans[spans < 1e-9] = 1.0

    mins = mins - padding
    maxs = maxs + padding

    return (
        float(mins[0]),
        float(mins[1]),
        float(mins[2]),
        float(maxs[0]),
        float(maxs[1]),
        float(maxs[2]),
    )


def render_scene(scene: Scene, output_path: str | None = None, show: bool = True, dpi: int = 180) -> Scene:
    scene._prepare()
    scene._draw_frames()
    scene.figure.canvas.draw()

    if output_path is not None:
        scene.figure.savefig(output_path, dpi=dpi, bbox_inches="tight")

    if show:
        Scene._show_plot()

    return scene


def get_task_output_path(image_index: int = 1, suffix: str = "png") -> str:
    this_file = Path(__file__).resolve()
    caller_file = this_file

    for frame_info in inspect.stack()[1:]:
        frame_path = Path(frame_info.filename).resolve()
        if frame_path.name.startswith("task") and frame_path.suffix == ".py":
            caller_file = frame_path
            break
        if frame_path != this_file:
            caller_file = frame_path

    stem = caller_file.stem
    return str(caller_file.with_name(f"{stem}_image_{image_index:02d}.{suffix}"))


def visualize_transform_3d(
    initial_vertices,
    transformation_matrix: np.ndarray | None = None,
    final_vertices=None,
    faces: list[tuple[int, ...]] | None = None,
    title: str = "3D transformation",
    coordinate_rect: tuple[float, float, float, float, float, float] | None = None,
    pivot=None,
    show_pivot: bool = False,
    show_local_frame: bool = False,
    output_path: str | None = None,
    show: bool = True,
):
    initial_vertices = _normalize_points(initial_vertices)

    if faces is None:
        faces = infer_faces_from_vertices(initial_vertices)

    if transformation_matrix is None and final_vertices is None:
        raise ValueError("either transformation_matrix or final_vertices must be provided")

    if final_vertices is None:
        final_vertices = homogeneous2standard(
            apply_transformation_matrix(
                transformation_matrix,
                standard2homogeneous(initial_vertices),
            )
        )
    else:
        final_vertices = _normalize_points(final_vertices)

    if coordinate_rect is None:
        coordinate_rect = get_coordinate_rect(initial_vertices, final_vertices)

    scene = Scene(
        coordinate_rect=coordinate_rect,
        title=title,
        grid_show=True,
        base_axis_show=False,
        axis_show=True,
    )

    original_model = MeshModel(
        initial_vertices,
        faces,
        color="lightgray",
        edge_color="gray",
        line_style="--",
        line_width=1.0,
        alpha=0.08,
    )

    final_model = MeshModel(
        initial_vertices if transformation_matrix is not None else final_vertices,
        faces,
        color="deepskyblue",
        edge_color="navy",
        line_style="-",
        line_width=1.3,
        alpha=0.18,
    )

    if pivot is not None:
        original_model.pivot(*pivot)
        final_model.pivot(*pivot)

    if show_pivot:
        original_model.show_pivot()
        final_model.show_pivot()

    if show_local_frame:
        original_model.show_local_frame()
        final_model.show_local_frame()

    if transformation_matrix is not None:
        final_model.transformation = to_engine_matrix(transformation_matrix)

    scene["initial_object"] = original_model
    scene["final_object"] = final_model

    return render_scene(scene, output_path=output_path, show=show)


def save_task_visualization(
    initial_vertices,
    transformation_matrix: np.ndarray | None = None,
    final_vertices=None,
    faces: list[tuple[int, ...]] | None = None,
    image_index: int = 1,
    title: str | None = None,
    coordinate_rect: tuple[float, float, float, float, float, float] | None = None,
    pivot=None,
    show_pivot: bool = False,
    show_local_frame: bool = False,
    show: bool = False,
):
    output_path = get_task_output_path(image_index=image_index)
    if title is None:
        title = Path(output_path).stem

    return visualize_transform_3d(
        initial_vertices=initial_vertices,
        transformation_matrix=transformation_matrix,
        final_vertices=final_vertices,
        faces=faces,
        title=title,
        coordinate_rect=coordinate_rect,
        pivot=pivot,
        show_pivot=show_pivot,
        show_local_frame=show_local_frame,
        output_path=output_path,
        show=show,
    )


def print_points(
    name: str,
    points,
    precision: int = 3,
    prefix: str = "P",
) -> None:
    normalized_points = _normalize_points(points)
    print(f"{name}:")
    for index, point in enumerate(normalized_points):
        x, y, z = point
        print(
            f"  {prefix}{index}: "
            f"({x:.{precision}f}, {y:.{precision}f}, {z:.{precision}f})"
        )
    print()


def print_step(
    title: str,
    matrix: np.ndarray | None = None,
    points=None,
    precision: int = 3,
    prefix: str = "P",
) -> None:
    print(f"=== {title} ===")
    if matrix is not None:
        print_matrix("M", matrix, precision)
    if points is not None:
        print_points("Vertices", points, precision=precision, prefix=prefix)


def print_step_sequence(
    initial_points,
    step_points: list,
    step_matrices: list[np.ndarray] | None = None,
    step_names: list[str] | None = None,
    precision: int = 3,
    prefix: str = "P",
) -> None:
    if step_names is None:
        step_names = [f"Step {index + 1}" for index in range(len(step_points))]

    if len(step_names) != len(step_points):
        raise ValueError("step_names and step_points must have the same length")

    if step_matrices is not None and len(step_matrices) != len(step_points):
        raise ValueError("step_matrices and step_points must have the same length")

    print_points("Initial vertices", initial_points, precision=precision, prefix=prefix)

    for index, points in enumerate(step_points):
        matrix = None if step_matrices is None else step_matrices[index]
        print_step(
            step_names[index],
            matrix=matrix,
            points=points,
            precision=precision,
            prefix=prefix,
        )


def print_matrix_chain(
    matrices: list[np.ndarray],
    names: list[str] | None = None,
    precision: int = 3,
    print_result: bool = True,
    result_name: str = "M_total",
) -> np.ndarray:
    if len(matrices) == 0:
        raise ValueError("matrices must contain at least one matrix")

    if names is not None and len(names) != len(matrices):
        raise ValueError("names and matrices must have the same length")

    print_matrices(matrices, precision=precision, names=names)

    result = np.eye(4)
    for matrix in matrices:
        result = matrix @ result

    if print_result:
        print_matrix(result_name, result, precision=precision)

    return result


def print_random_transform_parameters(
    angle_degrees: float,
    axis,
    translation,
    precision: int = 3,
) -> None:
    axis = np.asarray(axis, dtype=float)
    translation = np.asarray(translation, dtype=float)

    print("Random transform parameters:")
    print(f"  angle = {angle_degrees:.{precision}f} deg")
    print(
        f"  axis = ({axis[0]:.{precision}f}, {axis[1]:.{precision}f}, {axis[2]:.{precision}f})"
    )
    print(
        "  translation = "
        f"({translation[0]:.{precision}f}, {translation[1]:.{precision}f}, {translation[2]:.{precision}f})"
    )
    print()


def print_rotation_comparison(
    name_a: str,
    matrix_a: np.ndarray,
    name_b: str,
    matrix_b: np.ndarray,
    precision: int = 3,
    eps: float = 1e-6,
) -> None:
    print_matrix(name_a, matrix_a, precision)
    print_matrix(name_b, matrix_b, precision)

    are_equal = compare_rotation_matrices(matrix_a, matrix_b, eps=eps)
    print(f"{name_a} == {name_b}: {are_equal}")
    print()


def print_axis_angle(
    axis,
    angle_radians: float | None = None,
    angle_degrees: float | None = None,
    precision: int = 3,
) -> None:
    axis = np.asarray(axis, dtype=float)
    axis_norm = np.linalg.norm(axis)

    if not np.isclose(axis_norm, 0.0):
        axis = axis / axis_norm

    print(
        f"axis = ({axis[0]:.{precision}f}, {axis[1]:.{precision}f}, {axis[2]:.{precision}f})"
    )

    if angle_radians is not None:
        print(f"angle_rad = {angle_radians:.{precision}f}")

    if angle_degrees is not None:
        print(f"angle_deg = {angle_degrees:.{precision}f}")

    print()


def print_decomposition_report(
    matrix: np.ndarray,
    translation=None,
    rotation=None,
    scale=None,
    axis=None,
    angle_radians: float | None = None,
    angle_degrees: float | None = None,
    precision: int = 3,
) -> None:
    print_matrix("Affine matrix", matrix, precision)

    if translation is not None:
        translation = np.asarray(translation, dtype=float)
        print(
            "translation = "
            f"({translation[0]:.{precision}f}, {translation[1]:.{precision}f}, {translation[2]:.{precision}f})"
        )

    if scale is not None:
        scale = np.asarray(scale, dtype=float)
        print(
            f"scale = ({scale[0]:.{precision}f}, {scale[1]:.{precision}f}, {scale[2]:.{precision}f})"
        )

    if rotation is not None:
        print()
        print_matrix("Rotation", rotation, precision)
        print(f"rotation_is_orthogonal = {is_rotation_matrix(rotation)}")

    if axis is not None or angle_radians is not None or angle_degrees is not None:
        if rotation is not None:
            print()
        print_axis_angle(
            axis if axis is not None else [1.0, 0.0, 0.0],
            angle_radians=angle_radians,
            angle_degrees=angle_degrees,
            precision=precision,
        )
