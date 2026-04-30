import utils003 as utils


if __name__ == '__main__':
    cube = utils.get_cube_vertices()

    cube_homogenous = utils.standard2homogeneous(cube)

    S = utils.get_scale_matrix(2, 0.5, 1)
    R = utils.get_rotation_matrix_euler([30, 45, 60], "XYZ", "external")
    T = utils.get_translation_matrix(-3, 2, 5)

    cube_S = utils.apply_transformation_matrix(S, cube_homogenous)
    SR = R@S
    cube_SR = utils.apply_transformation_matrix(SR, cube_homogenous)
    SRT = T@R@S
    cube_SRT = utils.apply_transformation_matrix(SRT, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [cube_S, cube_SR, cube_SRT],
        [S, SR, SRT],
        ["After scale", "After Euler XYZ rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=SRT,
        faces=utils.get_cube_faces(),
        title="HW003 Task 001",
    )
