import utils003 as utils
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

    S = utils.get_scale_matrix(2, 0.5, 1)
    R = utils.get_rotation_matrix_euler([30, 45, 60], "XYZ", "external")
    T = utils.get_translation_matrix(-3, 2, 5)

    cube_S = utils.apply_transformation_matrix(S, cube_homogenous)
    SR = R@S
    cube_SR = utils.apply_transformation_matrix(SR, cube_homogenous)
    SRT = T@R@S
    cube_SRT = utils.apply_transformation_matrix(SRT, cube_homogenous)

