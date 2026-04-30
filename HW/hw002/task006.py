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
    RT = T@R
    cube_RT = utils.apply_transformation_matrix(RT, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [cube_R, cube_RT],
        [R, RT],
        ["After pivot rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=RT,
        faces=utils.get_cube_faces(),
        title="Task 006",
        pivot=[2, 0, 3],
        show_pivot=True,
    )
