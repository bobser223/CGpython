from gettext import translation

import numpy as np



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



if __name__ == "__main__":
    polygone_coordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous_coordinates = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    pivot = np.array([1, 1])

    scale = np.array([
        [2.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ])

    translation = np.array([
        [1.0, 0.0, 3.0],
        [0.0, 1.0, -2.0],
        [0.0, 0.0, 1.0],
    ])

    scale_translation = translation @ transformation_relative_to_pivot(scale, pivot)
    translation_scale = transformation_relative_to_pivot(scale, pivot) @ translation

    polygone_scale_translation = [
        (scale_translation @ vertex.reshape(3, 1))[0:2].flatten() for vertex in polygone_homogenous_coordinates
    ]

    polygone_translation_scale = [
        (translation_scale @ vertex.reshape(3, 1))[0:2].flatten() for vertex in polygone_homogenous_coordinates
    ]
    print(polygone_scale_translation)
    print(polygone_translation_scale)

