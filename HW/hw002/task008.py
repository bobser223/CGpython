import utils002 as utils
import numpy as np


if __name__ == '__main__':
    triangle = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ])
    triangle_homogeneous = utils.standard2homogeneous(triangle)

    R = utils.get_rotation_matrix(90.0, np.array([1.0, 1.0, 1.0]))
    R = utils.transformation_relative_to_pivot(R, np.array([2.0, 3.0, 4.0]))
    T = utils.get_translation_matrix(0.0, -3.0, 2.0)

    triangle_R = utils.apply_transformation_matrix(R, triangle_homogeneous)
    triangle_T = utils.apply_transformation_matrix(T, triangle_homogeneous)

    RT = T@R
    triangle_RT = utils.apply_transformation_matrix(RT, triangle_homogeneous)
