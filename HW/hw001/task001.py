import os.path

import numpy as np
import utils




if __name__ == '__main__':
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogeneous = utils.standard2homogeneous(polygone)

    rotation = utils.get_rotation_matrix(30)
    translation = utils.get_translation_matrix(2, 3)

    polygone_rotated = utils.apply_transformation_matrix(rotation, polygone_homogeneous)
    polygone_translated = utils.apply_transformation_matrix(translation, polygone_homogeneous)
    RT = translation @ rotation
    polygone_rotated_translated = utils.apply_transformation_matrix(RT, polygone_homogeneous)

    utils.draw_polygone_no_pivot(polygone, utils.homogeneous2standard(polygone_rotated_translated), "task001_image_01")