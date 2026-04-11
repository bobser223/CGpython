import numpy as np
import utils

if __name__ == '__main__':
    TRS = np.array([
        [1.414, -2.121, 1.0],
        [1.414, 2.121, 1.0],
        [0.0, 0.0, 1.0]
    ])

    poligon = np.array([[0,0], [1,0], [1,1], [0,1]])
    poligon_homogeneous = utils.standard2homogeneous(poligon)


    translation, rotation , scale = utils.decompose_TRS(TRS)
    utils.print_matrices([rotation, scale, translation], names=["R", "S", "T"])

    poligon_transformed= utils.apply_transformation_matrix(TRS, poligon_homogeneous)
    print(poligon_transformed)

    utils.draw_polygone_no_pivot(poligon, utils.homogeneous2standard(poligon_transformed), "task013_image_01", )


    # print(polygon_local)




