import numpy as np
import utils

if __name__ == '__main__':
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogeneous = utils.standard2homogeneous(polygone)


    scale = utils.get_scale_matrix(1, 3)
    rotation = utils.get_rotation_matrix(60)

    polygone_scaled = utils.apply_transformation_matrix(scale, polygone_homogeneous)
    polygone_rotated = utils.apply_transformation_matrix(rotation, polygone_homogeneous)

    SR = rotation @ scale

    polygone_scaled_rotated = utils.apply_transformation_matrix(SR, polygone_homogeneous)
    utils.draw_polygone_no_pivot(polygone, utils.homogeneous2standard(polygone_scaled_rotated), "task004_image_01")