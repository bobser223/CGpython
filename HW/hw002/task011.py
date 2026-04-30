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
    R_A = utils.get_rotation_matrix_euler([30, 45, 60], "ZYX", "external")
    R_B = utils.get_rotation_matrix_euler([60, 45, 30], "XYZ", "internal")


    if (utils.compare_rotation_matrices(R_A, R_B)):
        print("Matrices are equal")
    else:
        print("Matrices are not equal")

    cube_RA = utils.apply_transformation_matrix(R_A, cube_homogenous)
    cube_RB = utils.apply_transformation_matrix(R_B, cube_homogenous)

    utils.print_rotation_comparison("R_A", R_A, "R_B", R_B)
    utils.print_points("Vertices after external rotation", cube_RA)
    utils.print_points("Vertices after internal rotation", cube_RB)

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=R_A,
        faces=utils.get_cube_faces(),
        title="Task 011 A",
        image_index=1,
    )
    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=R_B,
        faces=utils.get_cube_faces(),
        title="Task 011 B",
        image_index=2,
    )
