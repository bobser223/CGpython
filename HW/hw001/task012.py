import numpy as np
import utils

if __name__ == '__main__':
    TRS = np.array([
        [0.866, 0.5, 4],
        [0.5, 0.866, 3],
        [0.0, 0.0, 1.0]
    ])

    poligon = np.array([[0,0], [1,0], [1,1], [0,1]])
    poligon_homogeneous = utils.standard2homogeneous(poligon)


    # translation, rotation , scale = utils.TRS_decomposition(TRS) # not a rotation matrix
    #/HW/hw001/utils.py", line 81, in TRS_decomposition
    #raise ValueError("This matrix cannot be decomposed into pure T, R, S with diagonal scale.")
    #ValueError: This matrix cannot be decomposed into pure T, R, S with diagonal scale.

    # utils.print_matrices([rotation, scale, translation], names=["R", "S", "T"])

    poligon_transformed= utils.apply_transformation_matrix(TRS, poligon_homogeneous)
    print(poligon_transformed)

    utils.draw_polygone_tasks_1_6(poligon, utils.homogeneous2standard(poligon_transformed), "task012_image_01", (-2,-2, 6, 7))
    # в принципі по картинці видно що геометрія зламалась -> бяка

    # print(polygon_local)




