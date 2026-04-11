import numpy as np
import utils

if __name__ == '__main__':
    TRS = np.array([
        [2.934, -0.416, 2.000],
        [0.624, 1.956, 3.400],
        [0.0, 0.0, 1.0]
    ])

    poligon = np.array([[2,3.4],[4.9,4],[4.5,6],[1.6,5.4]])
    poligon_homogeneous = utils.standard2homogeneous(poligon)


    translation, rotation , scale = utils.decompose_TRS(TRS)
    rev_translation = utils.inverse_translation_matrix(translation)
    rev_rotation = utils.inverse_rotation_matrix(rotation)
    rev_scale = utils.inverse_scale_matrix(scale)

    rev_TRS = rev_scale @ rev_rotation @ rev_translation
    poligon_homogeneous_rev = utils.apply_transformation_matrix(rev_TRS, poligon_homogeneous)

    poligon_local = utils.homogeneous2standard(poligon_homogeneous_rev)
    print(poligon_local)

    utils.draw_polygone_tasks_1_6(poligon_local, poligon, "task011_image_01", (-2,-2, 6, 7))




