import numpy as np
import utils



if __name__ == "__main__":
    polygone_coordinates = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    polygone_homogenous_coordinates = np.array(
        [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    )

    scale = utils.get_scale_matrix(2, 2)
    rotation = utils.get_rotation_matrix(30)
    translation = utils.get_translation_matrix(1, -1)

    #o Масштабування → Обертання → Зсув.

    #o Зсув → Масштабування → Обертання.

    #o Масштабування → Зсув → Обертання.

    scale_rotation_translation = translation @ rotation @ scale
    translation_scale_rotation = rotation @ scale @ translation
    scale_translation_rotation = rotation @ translation @ scale


    new_polygons = []
    for matrix in [scale_rotation_translation, translation_scale_rotation, scale_translation_rotation]:
        new_polygons.append(utils.apply_transformation_matrix(matrix, polygone_homogenous_coordinates))




