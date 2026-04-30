import utils003 as utils

if __name__ == '__main__':
    cube = utils.get_cube_vertices()

    cube_homogenous = utils.standard2homogeneous(cube)
    R = utils.get_rotation_matrix_euler([ 20, 35, 50], "ZYX", "external")
    T = utils.get_translation_matrix(1, 3, -2)

    cube_R = utils.apply_transformation_matrix(R, cube_homogenous)
    RT = T@R
    cube_RT = utils.apply_transformation_matrix(RT, cube_homogenous)

    utils.print_step_sequence(
        cube,
        [cube_R, cube_RT],
        [R, RT],
        ["After Euler ZYX rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=cube,
        transformation_matrix=RT,
        faces=utils.get_cube_faces(),
        title="HW003 Task 002",
    )
