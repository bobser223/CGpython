import utils002 as utils
import numpy as np


if __name__ == '__main__':
    tetrahedron = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])

    tetrahedron_homogeneous = utils.standard2homogeneous(tetrahedron)
    R_local_1 = utils.get_rotation_matrix(45, np.array([1, 0, 0]))
    T_local = utils.get_translation_matrix(2, 0,0)
    R_local_2 = utils.get_rotation_matrix(30, np.array([1,0, 0]))

    full_chain = R_local_1 @ T_local @ R_local_2
    full_chain = R_local_1 @ T_local @ R_local_2
    # correct for intrinsic composition if we appended operations in this order:
    # M = I
    # M = M @ R_local_1
    # M = M @ T_local
    # M = M @ R_local_2

    tet_R1 = utils.apply_transformation_matrix(R_local_1, tetrahedron_homogeneous)
    tet_R1T = utils.apply_transformation_matrix(R_local_1@T_local, tetrahedron_homogeneous)
    tetrahedron_full_chain = utils.apply_transformation_matrix(full_chain, tetrahedron_homogeneous)

    utils.print_step_sequence(
        tetrahedron,
        [tet_R1, tet_R1T, tetrahedron_full_chain],
        [R_local_1, R_local_1 @ T_local, full_chain],
        ["After local rotation", "After local translation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=tetrahedron,
        transformation_matrix=full_chain,
        faces=utils.get_tetrahedron_faces(),
        title="Task 013",
    )
