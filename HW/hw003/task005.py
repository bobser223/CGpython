import utils003 as utils

if __name__ == '__main__':
    cube = utils.get_cube_vertices()

    cube_homogenous = utils.standard2homogeneous(cube)

    R = utils.get_rotation_matrix_euler([30, 90, 45], "XYZ", "internal")
    cube_R = utils.apply_transformation_matrix(R, cube_homogenous)
    R2 = utils.get_rotation_matrix_euler([40, 90, 35], "XYZ", "internal")
    cube_R2 = utils.apply_transformation_matrix(R2, cube_homogenous)

    utils.print_rotation_comparison("R_base", R, "R_modified", R2)
    utils.print_points("Vertices for base orientation", cube_R)
    utils.print_points("Vertices for modified angles", cube_R2)
    print(f"same_orientation = {utils.compare_rotation_matrices(R, R2)}")
    print()

    utils.save_task_multiple_visualization(
        objects=[
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "transformation_matrix": R,
                "color": "deepskyblue",
                "edge_color": "navy",
                "alpha": 0.16,
            },
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "transformation_matrix": R2,
                "color": "salmon",
                "edge_color": "darkred",
                "alpha": 0.10,
            },
        ],
        title="HW003 Task 005",
    )
