import numpy as np
import utils

if __name__ == '__main__':
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogeneous = utils.standard2homogeneous(polygone)

    scale = utils.get_scale_matrix(2, 1)
    rotation = utils.get_rotation_matrix(45)

    polygone_scaled = utils.apply_transformation_matrix(scale, polygone_homogeneous)
    polygone_rotated = utils.apply_transformation_matrix(rotation, polygone_homogeneous)

    SR = rotation @ scale
    polygone_scaled_rotated = utils.apply_transformation_matrix(SR, polygone_homogeneous)
    utils.draw_polygone_tasks_1_6(polygone, utils.homogeneous2standard(polygone_scaled_rotated), "task002_image_01")

