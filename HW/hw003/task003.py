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


    R1 = utils.get_rotation_matrix_euler([ 45,30, 60], "XYZ", "external") # x = 45, y = 30, z = 60
    R2 = utils.get_rotation_matrix_euler([ 45, 30, 60], "ZYX", "external") # z = 45, y = 30, x = 60

    cube_R1 = utils.apply_transformation_matrix(R1, cube_homogenous)
    cube_R2 = utils.apply_transformation_matrix(R2, cube_homogenous)

    utils.print_matrix("XYZ", R1)
    utils.print_matrix("ZYX", R2)
    print(cube_R1)
    print(cube_R2)



