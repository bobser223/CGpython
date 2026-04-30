import numpy as np
import utils002 as utils


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


    rotation = utils.get_rotation_matrix(45, np.array([1, 1, 0]))
    translation = utils.get_translation_matrix(2, -1, 3)

    cube_R = utils.apply_transformation_matrix(rotation, cube_homogenous)

    RT = translation@rotation

    cube_RT = utils.apply_transformation_matrix(RT, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [cube_R, cube_RT],
        [rotation, RT],
        ["After rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=RT,
        faces=utils.get_cube_faces(),
        title="Task 001",
    )
