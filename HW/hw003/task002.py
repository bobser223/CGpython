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
    R = utils.get_rotation_matrix_euler([ 20, 35, 50], "ZYX", "external")
    T = utils.get_translation_matrix(1, 3, -2)

    cube_R = utils.apply_transformation_matrix(R, cube_homogenous)
    cube_T = utils.apply_transformation_matrix(T, cube_homogenous)
    RT = T@R
    cube_RT = utils.apply_transformation_matrix(RT, cube_homogenous)
