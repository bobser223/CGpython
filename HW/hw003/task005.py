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

    R = utils.get_rotation_matrix_euler([ 30,90,45], "XYZ", "external")
    cube_R = utils.apply_transformation_matrix(R, cube_homogenous)
    R2 = utils.get_rotation_matrix_euler([ 30+10,90,45-10], "XYZ", "external")
    cube_R2 = utils.apply_transformation_matrix(R2, cube_homogenous)

    for c1, c2 in zip(cube_R, cube_R2):
        print(f"c1: {c1} == c2: {c2}")