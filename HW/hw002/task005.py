import utils002 as utils
import numpy as np


def get_rand_number(min, max):
    return np.random.uniform(
        min, max
    )

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

    rand_deg = np.random.uniform(10, 90)
    rand_axis = np.random.uniform(-1, 1, 3)
    rand_t_vec = np.random.uniform(-5, 5, 3)

    R = utils.get_rotation_matrix(rand_deg, rand_axis)
    T = utils.get_translation_matrix(rand_t_vec[0], rand_t_vec[1], rand_t_vec[2])
    cube_R = utils.apply_transformation_matrix(R, cube_homogenous)
    cube_T = utils.apply_transformation_matrix(T, cube_homogenous)

    RT = T@R
    cube_RT = utils.apply_transformation_matrix(RT, cube_homogenous)

