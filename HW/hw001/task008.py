import numpy as np
import utils


if __name__ == "__main__":
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    pivots = np.array([[0.5, 0.5], [0, 1], [1, 1], [2, 2]])
    scale = utils.get_scale_matrix(2, 3)

    R_1 = utils.transformation_relative_to_pivot(scale, pivots[0])
    R_2 = utils.transformation_relative_to_pivot(scale, pivots[1])
    R_3 = utils.transformation_relative_to_pivot(scale, pivots[2])
    R_4 = utils.transformation_relative_to_pivot(scale, pivots[3])

    polygone_scaled_1 = utils.apply_transformation_matrix(R_1, polygone_homogenous)
    polygone_scaled_2 = utils.apply_transformation_matrix(R_2, polygone_homogenous)
    polygone_scaled_3 = utils.apply_transformation_matrix(R_3, polygone_homogenous)
    polygone_scaled_4 = utils.apply_transformation_matrix(R_4, polygone_homogenous)

    utils.draw_polygone_tasks_7_10(polygone, utils.homogeneous2standard(polygone_scaled_1), pivots[0], "task008_image_01")
    utils.draw_polygone_tasks_7_10(polygone, utils.homogeneous2standard(polygone_scaled_2), pivots[1], "task008_image_02")
    utils.draw_polygone_tasks_7_10(polygone, utils.homogeneous2standard(polygone_scaled_3), pivots[2], "task008_image_03")
    utils.draw_polygone_tasks_7_10(polygone, utils.homogeneous2standard(polygone_scaled_4), pivots[3], "task008_image_04")