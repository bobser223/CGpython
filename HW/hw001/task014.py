import numpy as np
import utils
if __name__ == '__main__':
    # TRS = T*T(pivot)*R*S*T(-pivot)
    TRS = np.array([
        [1.732, -1.0, 5.0],
        [1.0, 1.732, -3.0],
        [0.0, 0.0, 1.0]
    ])



    translation, rotation, scale = utils.decompose_TRS(TRS)
    RS = rotation @ scale

    pivot = np.array([1.0, 1.0])
    RS_pivot = utils.transformation_relative_to_pivot(RS, pivot)

    # TRS = T*RS_pivot -> T = TRS*RS_pivot^-1
    translation_new = TRS @ np.linalg.inv(RS_pivot)

    TRS_check = translation_new @ RS_pivot

    print(TRS_check)

    poligon = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    poligon_homogeneous = utils.standard2homogeneous(poligon)

    utils.draw_polygone_tasks_1_6(poligon,
    utils.homogeneous2standard(utils.apply_transformation_matrix(TRS, poligon_homogeneous))
    , "task014_image_01", (-1,-6, 8, 2))


