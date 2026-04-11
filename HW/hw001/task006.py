import numpy as np
import utils

if __name__ == '__main__':
    polygone = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogeneous = utils.standard2homogeneous(polygone)

    scale = utils.get_scale_matrix(1, 3)
    rotation = utils.get_rotation_matrix(60)
    translation = utils.get_translation_matrix(2, 3)

    SRT = translation @ rotation @ scale
    polygone_SRT = utils.apply_transformation_matrix(SRT, polygone_homogeneous)
    TSR =  rotation @ scale @ translation
    polygone_TSR = utils.apply_transformation_matrix(TSR, polygone_homogeneous)

    polygone_rotated = utils.apply_transformation_matrix(rotation, polygone_homogeneous)
    polygone_scaled = utils.apply_transformation_matrix(scale, polygone_homogeneous)
    polygone_translated = utils.apply_transformation_matrix(translation, polygone_homogeneous)

    SR = rotation @ scale
    polygone_scaled_rotated = utils.apply_transformation_matrix(SR, polygone_homogeneous)
    TS = scale @ translation
    polygone_translated_scaled = utils.apply_transformation_matrix(TS, polygone_homogeneous)
