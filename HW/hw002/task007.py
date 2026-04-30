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
    S = utils.get_scale_matrix(1, 1, 3)
    S = utils.transformation_relative_to_pivot(S, np.array([1,2, 3]))
    R = utils.get_rotation_matrix(30, np.array([0,0,1]))
    R = utils.transformation_relative_to_pivot(R, np.array([1,2, 3]))

    cube_S = utils.apply_transformation_matrix(S, cube_homogenous)
    SR = R@S
    cube_SR = utils.apply_transformation_matrix(SR, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [cube_S, cube_SR],
        [S, SR],
        ["After pivot scale", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=SR,
        faces=utils.get_cube_faces(),
        title="Task 007",
        pivot=[1, 2, 3],
        show_pivot=True,
    )
