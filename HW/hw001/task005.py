import numpy as np
import utils

if __name__ == '__main__':
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogeneous = utils.standard2homogeneous(polygone)

    translation = utils.get_translation_matrix(1, -1)
    scale = utils.get_scale_matrix(2, 2)

    polygone_translated = utils.apply_transformation_matrix(translation, polygone_homogeneous)
    polygone_scaled = utils.apply_transformation_matrix(scale, polygone_homogeneous)
    TS = scale @ translation
    polygone_translated_scaled = utils.apply_transformation_matrix(TS, polygone_homogeneous)
    utils.draw_polygone_tasks_1_6(polygone, utils.homogeneous2standard(polygone_translated_scaled), "task005_image_01")