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

    R = utils.get_rotation_matrix(45, np.array([0, 1, 0]))
    R = utils.transformation_relative_to_pivot(R, np.array([2, 0, 3]))
    T = utils.get_translation_matrix(-1, 2, 4)

    cube_R = utils.apply_transformation_matrix(R, cube_homogenous)
    cube_T = utils.apply_transformation_matrix(T, cube_homogenous)

    RT = T@R
    cube_RT = utils.apply_transformation_matrix(RT, cube_homogenous)

    print(
        "Cube after applying rotation and translation:\n",
        cube_RT
    )