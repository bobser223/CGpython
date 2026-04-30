import utils003 as utils


def interpolate_angles(start_angles, end_angles, steps) -> list[list[float]]:
    return [
        [
            (1 - step / steps) * start_angle + (step / steps) * end_angle
            for start_angle, end_angle in zip(start_angles, end_angles)
        ]
        for step in range(1, steps + 1)
    ]


if __name__ == "__main__":
    interpolated_angles = interpolate_angles(
        [0, 0, 0],
        [90, 90, 90],
        10
    )

    look_vector = [0.0, 0.0, 1.0]

    look_vectors = []
    tip_positions = []

    for angles in interpolated_angles:
        R = utils.get_rotation_matrix_euler(angles, "XYZ", "internal")

        transformed_look = utils.transform_direction(R, look_vector)

        look_vectors.append(transformed_look)
        tip_positions.append(transformed_look)

        print("angles:", angles)
        utils.print_matrix("R", R)
        print("look:", transformed_look)
        print()

    utils.print_angle_sequence("Interpolated Euler angles", interpolated_angles)
    utils.save_task_trajectory_visualization(
        trajectory_points=tip_positions,
        arrows=[
            {"start": [0.0, 0.0, 0.0], "end": tip, "label": f"{index + 1}"}
            for index, tip in enumerate(tip_positions)
        ],
        title="HW003 Task 006",
    )
