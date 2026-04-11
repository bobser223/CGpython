import numpy as np


def get_transformation_matrix(a: float, b: float) -> np.ndarray:
    translate_to_origin = np.array(
        [
            [1.0, 0.0, -a],
            [0.0, 1.0, -b],
            [0.0, 0.0, 1.0],
        ]
    )
    scale = np.array(
        [
            [2.0, 0.0, 0.0],
            [0.0, 3.0, 0.0],
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
    return translate_back @ scale @ translate_to_origin


if __name__ == "__main__":
    polygone_coordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous_coordinates = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    pivots = np.array([[0.5, 0.5], [0, 1], [1, 1], [2, 2]])
    transformation_matrices = []
    for pivot in pivots:
        transformation_matrices.append(get_transformation_matrix(pivot[0], pivot[1]))
        print(
            f"transformation Matrix for pivot: {pivot[0], pivot[1]} =\n {transformation_matrices[-1]}"
        )
        for i in range(4):
            print(
                f"Point {i} = {transformation_matrices[-1] @ polygone_homogenous_coordinates[i]}"
            )
