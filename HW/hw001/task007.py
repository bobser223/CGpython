import numpy as np


def get_transformation_matrix(a: float, b: float) -> np.ndarray:
    # a, b are coordinates of the pivot point

    translate_to_origin = np.array(
        [
            [1.0, 0.0, -a],
            [0.0, 1.0, -b],
            [0.0, 0.0, 1.0],
        ]
    )

    cos_60 = np.cos(np.deg2rad(60))
    sin_60 = np.sin(np.deg2rad(60))
    rotation = np.array([[cos_60, -sin_60, 0.0], [sin_60, cos_60, 0.0], [0.0, 0.0, 1]])

    translate_back = np.array(
        [
            [1.0, 0.0, a],
            [0.0, 1.0, b],
            [0.0, 0.0, 1.0],
        ]
    )

    return translate_back @ rotation @ translate_to_origin


if __name__ == "__main__":
    polygoneCoordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous_coordinates = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    pivots = np.array([[0.5, 0.5], [0, 1], [1, 1], [2, 2]])
    transformationMatrices = []
    for pivot in pivots:
        transformationMatrices.append(get_transformation_matrix(pivot[0], pivot[1]))
        print(
            f"transformation Matrix for pivot: {pivot[0], pivot[1]} =\n {transformationMatrices[-1]}"
        )
        for i in range(4):
            print(
                f"Point {i} = {transformationMatrices[-1] @ polygone_homogenous_coordinates[i]}"
            )
