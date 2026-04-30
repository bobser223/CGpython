import utils002 as utils
import numpy as np


if __name__ == '__main__':
    rectangle = np.array([[1, 2, 0], [4, 2, 0], [4, 5, 0], [1, 5, 0]])
    rectangle_homogeneous = utils.standard2homogeneous(rectangle)

    R1 = utils.get_rotation_matrix_y(60.0)
    R1 = utils.transformation_relative_to_pivot(R1, np.array([3.0, 3.0, 0.0]))
    R2 = utils.get_rotation_matrix_x(30)
    R2 = utils.transformation_relative_to_pivot(R2, np.array([3.0, 3.0, 0.0]))

    rectangle_R1 = utils.apply_transformation_matrix(R1, rectangle_homogeneous)

    R1R2 = R2@R1
    rectangle_R1R2 = utils.apply_transformation_matrix(R1R2, rectangle_homogeneous)

    utils.print_step_sequence(
        rectangle,
        [rectangle_R1, rectangle_R1R2],
        [R1, R1R2],
        ["After Y pivot rotation", "Final state"],
    )

    utils.save_task_visualization(
        initial_vertices=rectangle,
        transformation_matrix=R1R2,
        title="Task 009",
        pivot=[3, 3, 0],
        show_pivot=True,
    )
