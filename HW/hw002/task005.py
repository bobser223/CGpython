import utils002 as utils
import numpy as np

if __name__ == '__main__':
    tetrahedron = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ])

    tetrahedron_homogenous = utils.standard2homogeneous(tetrahedron)

    rand_deg = np.random.uniform(10, 90)
    rand_axis = np.random.uniform(-1, 1, 3)
    rand_t_vec = np.random.uniform(-5, 5, 3)

    R = utils.get_rotation_matrix(rand_deg, rand_axis)
    T = utils.get_translation_matrix(rand_t_vec[0], rand_t_vec[1], rand_t_vec[2])
    tetrahedron_R = utils.apply_transformation_matrix(R, tetrahedron_homogenous)

    RT = T@R
    tetrahedron_RT = utils.apply_transformation_matrix(RT, tetrahedron_homogenous)

    utils.print_random_transform_parameters(rand_deg, rand_axis, rand_t_vec)
    utils.print_step_sequence(
        tetrahedron,
        [tetrahedron_R, tetrahedron_RT],
        [R, RT],
        ["After random rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=tetrahedron,
        transformation_matrix=RT,
        faces=utils.get_tetrahedron_faces(),
        title="Task 005",
    )
