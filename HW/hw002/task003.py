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

    R1 = utils.get_rotation_matrix(60, np.array([0,0,1]))
    R2 = utils.get_rotation_matrix(45, np.array([1, 1, 1]))
    T = utils.get_translation_matrix(4, -2, 1)

    R1R2 = R2@R1
    cube_R1R2 = utils.apply_transformation_matrix(R1R2, cube_homogenous)

    R1R2T = T@R2@R1
    cube_R1R2T = utils.apply_transformation_matrix(R1R2T, cube_homogenous)

    