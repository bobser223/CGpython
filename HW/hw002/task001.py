import utils002
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

    cube_homogenous = utils002.standard2homogeneous(cube)


    rotation = utils002.get_rotation_matrix(45, np.array([1, 1, 0]))
    translation = utils002.get_translation_matrix(2, -1, 3)

    cube_R = utils002.apply_transformation_matrix(rotation, cube_homogenous)
    cube_T = utils002.apply_transformation_matrix(translation, cube_homogenous)

    RT = translation@rotation

    cube_RT = utils002.apply_transformation_matrix(RT, cube_homogenous)


