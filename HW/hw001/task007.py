import numpy as np
import utils


if __name__ == "__main__":
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    pivots = np.array([[0.5, 0.5], [0, 1], [1, 1], [2, 2]])
    rotation = utils.get_rotation_matrix(60)

    R_1 = utils.transformation_relative_to_pivot(rotation, pivots[0])
    R_2 = utils.transformation_relative_to_pivot(rotation, pivots[1])
    R_3 = utils.transformation_relative_to_pivot(rotation, pivots[2])
    R_4 = utils.transformation_relative_to_pivot(rotation, pivots[3])

    polygone_rotated_1 = utils.apply_transformation_matrix(R_1, polygone_homogenous)
    polygone_rotated_2 = utils.apply_transformation_matrix(R_2, polygone_homogenous)
    polygone_rotated_3 = utils.apply_transformation_matrix(R_3, polygone_homogenous)
    polygone_rotated_4 = utils.apply_transformation_matrix(R_4, polygone_homogenous)

    utils.draw_polygone_with_pivot(polygone, utils.homogeneous2standard(polygone_rotated_1), pivots[0], "task007_image_01")
    utils.draw_polygone_with_pivot(polygone, utils.homogeneous2standard(polygone_rotated_2), pivots[1], "task007_image_02")
    utils.draw_polygone_with_pivot(polygone, utils.homogeneous2standard(polygone_rotated_3), pivots[2], "task007_image_03")
    utils.draw_polygone_with_pivot(polygone, utils.homogeneous2standard(polygone_rotated_4), pivots[3], "task007_image_04")