import numpy as np
import utils

if __name__ == "__main__":
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    pivot = np.array([1, 1])

    scale = utils.get_scale_matrix(2, 1)

    translation = utils.get_translation_matrix(3, -2)

    ST = translation @ utils.transformation_relative_to_pivot(scale, pivot)
    TS = utils.transformation_relative_to_pivot(scale, pivot) @ translation

    polygone_ST = utils.apply_transformation_matrix(ST, polygone_homogenous)
    polygone_TS = utils.apply_transformation_matrix(TS, polygone_homogenous)
    utils.draw_polygone_with_pivot(polygone, utils.homogeneous2standard(polygone_ST), pivot, "task009_image_01")
    utils.draw_polygone_with_pivot(polygone, utils.homogeneous2standard(polygone_TS), pivot, "task009_image_02", (-1, -4, 8, 4))

