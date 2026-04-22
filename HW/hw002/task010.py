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

    S = utils.get_scale_matrix(2, 1, 1)
    S = utils.transformation_relative_to_pivot(S, [1,1,1])
    R = utils.get_rotation_matrix_y(45)
    R = utils.transformation_relative_to_pivot(R, [1,1,1])
    T = utils.get_translation_matrix(-3, 4, 2)

    cube_S = utils.apply_transformation_matrix(cube, S)

    SR = R @ S
    cube_SR = utils.apply_transformation_matrix(cube, SR)

    SRT = T@R@S
    cube_SRT = utils.apply_transformation_matrix(cube, SRT)

    