import utils003 as utils

if __name__ == '__main__':
    cube = utils.get_cube_vertices()

    cube_homogenous = utils.standard2homogeneous(cube)

    R1 = utils.get_rotation_matrix_euler([ 45,30, 60], "XYZ", "external") # x = 45, y = 30, z = 60
    R2 = utils.get_rotation_matrix_euler([ 45, 30, 60], "ZYX", "external") # z = 45, y = 30, x = 60

    cube_R1 = utils.apply_transformation_matrix(R1, cube_homogenous)
    cube_R2 = utils.apply_transformation_matrix(R2, cube_homogenous)

    utils.print_rotation_comparison("R_XYZ_external", R1, "R_ZYX_external", R2)
    utils.print_points("Vertices after XYZ external rotation", cube_R1)
    utils.print_points("Vertices after ZYX external rotation", cube_R2)
    print("Explanation: identical angle triples do not give the same orientation because matrix multiplication is non-commutative.")
    print()

    utils.save_task_multiple_visualization(
        objects=[
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "color": "lightgray",
                "edge_color": "gray",
                "line_style": "--",
                "alpha": 0.06,
            },
            {
                "vertices": cube,
                "faces": utils.get_cube_faces(),
                "transformation_matrix": R1,
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
                "alpha": 0.16,
            },
        ],
        title="HW003 Task 003",
    )


