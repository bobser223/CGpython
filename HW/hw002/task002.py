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

    scale = utils.get_scale_matrix(2, 0.5, 1)
    rotation = utils.get_rotation_matrix_euler([30, 45, 60], "ZYX")
    translation = utils.get_translation_matrix(-3, 2, 5)

    cube_S = utils.apply_transformation_matrix(scale, cube_homogenous)
    SR = rotation @ scale
    STR = translation @ rotation @ scale

    cube_SR = utils.apply_transformation_matrix(SR, cube_homogenous)
    cube_STR = utils.apply_transformation_matrix(STR, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [cube_S, cube_SR, cube_STR],
        [scale, SR, STR],
        ["After scale", "After scale + Euler rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=STR,
        faces=utils.get_cube_faces(),
        title="Task 002",
    )
