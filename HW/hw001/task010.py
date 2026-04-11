import numpy as np
import utils



if __name__ == "__main__":
    polygone_coordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous_coordinates = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )
    pivot = np.array([0.5, 0.5])

    scale = utils.get_scale_matrix(2, 2)
    rotation = utils.get_rotation_matrix(30)
    translation = utils.get_translation_matrix(1, -1)


    scale_rotation_translation = translation @ rotation @ scale
    translation_scale_rotation = rotation @ scale @ translation
    scale_translation_rotation = rotation @ translation @ scale


    new_polygons = []
    for matrix in [scale_rotation_translation, translation_scale_rotation, scale_translation_rotation]:
        new_polygons.append(utils.apply_transformation_matrix(matrix, polygone_homogenous_coordinates))

    utils.draw_polygone_tasks_7_10(polygone_coordinates, utils.homogeneous2standard(new_polygons[0]),pivot, "task010_image_01")
    utils.draw_polygone_tasks_7_10(polygone_coordinates, utils.homogeneous2standard(new_polygons[1]),pivot, "task010_image_02")
    utils.draw_polygone_tasks_7_10(polygone_coordinates, utils.homogeneous2standard(new_polygons[2]),pivot, "task010_image_03")





