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
    S = utils.get_scale_matrix(2, 2, 2)
    S = utils.transformation_relative_to_pivot(S, np.array([1,1, 1]))
    R = utils.get_rotation_matrix_x(90) #make it local <-> intrinsic
    T = utils.get_translation_matrix(-3, 4, 2)
    # M = I
    # M = S @ M
    # M = M @ R
    # M = T @ M
    M = np.eye(4)
    M = S @ M
    M = M @ R
    M = T @ M
    cube_M = utils.apply_transformation_matrix(M, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [utils.apply_transformation_matrix(S, cube_homogenous), utils.apply_transformation_matrix(S @ R, cube_homogenous), cube_M],
        [S, S @ R, M],
        ["After pivot scale", "After local rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=M,
        faces=utils.get_cube_faces(),
        title="Task 015",
        pivot=[1, 1, 1],
        show_pivot=True,
    )
