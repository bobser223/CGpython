import utils002 as utils
import numpy as np


if __name__ == '__main__':
    cube = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0],
    ])

    cube_homogenous = utils.standard2homogeneous(cube)

    scale = utils.get_scale_matrix(2, 0.5, 1)
    rotation = utils.get_rotation_matrix_euler([30, 45, 60], "ZYX")
    translation = utils.get_translation_matrix(-3, 2, 5)

    cube_S = utils.apply_transformation_matrix(scale, cube_homogenous)
    cube_R = utils.apply_transformation_matrix(rotation, cube_homogenous)
    cube_T = utils.apply_transformation_matrix(translation, cube_homogenous)

    ST = translation@scale
    SR = rotation@scale
    RT = translation@rotation
    STR = rotation@translation@scale
    TRS = scale@rotation@translation
    RTS = scale@translation@rotation

    cube_ST = utils.apply_transformation_matrix(ST, cube_homogenous)
    cube_STR = utils.apply_transformation_matrix(STR, cube_homogenous)

