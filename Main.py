#
# import Solver
# from ErrorTypes import SolverError
#
# game_version = "1.2.0"
#
# if __name__ == "__main__":
#
#     start_message = "############################\n"
#     start_message += "WELCOME IN SUDOKU SOLVER " + game_version + "\n"
#     start_message += "############################\n"
#
#     print(start_message)
#
#     # crea il risolutore
#     solver = Solver.Solver()
#     # avvia il gioco
#     ret_code = solver.solve()
#
#     if ret_code != SolverError.OK:
#         print(solver.get_error_description(ret_code))
#


import cv2
import numpy as np
from numpy.ma.extras import row_stack


def is_square(contour):
    # valuta la prima condizione per avere un rettangolo ovvero che larghezza e altezza sono circa uguali
    _,_,w,h = cv2.boundingRect(contour)
    aspect_ratio = w/h
    is_aspect_ratio_almost_one = 0.95 < aspect_ratio < 1.05
    #valuta la seconda condizione ovvero che il perimetro sia circa uguale al doppio di una delle dimensioni
    perimeter = cv2.arcLength(contour,True)
    is_a_square_perimeter = 0.95 * 4 * w < perimeter < 1.05 * 4 * w
    return is_aspect_ratio_almost_one and is_a_square_perimeter

if __name__ == "__main__":
    grid_paths = ["grid.jpg","grid1.jpg","grid2.jpg","grid3.png","grid4.png","grid5.png"]
    for image_path in grid_paths:
        # legge l'immagine in bianco e nero e la scala
        input_grid_original = cv2.imread(image_path)
        input_grid = cv2.cvtColor(input_grid_original, cv2.COLOR_BGR2GRAY)
        input_grid_original = cv2.resize(input_grid_original, None, fx=0.75,fy=0.75)
        input_grid = cv2.resize(input_grid, None, fx=0.75,fy=0.75)

        # filtra l'immagine
        input_grid = cv2.medianBlur(input_grid,3)

        # crea un'immagine binaria che evidenzia griglia e contorni
        threshold = cv2.adaptiveThreshold(input_grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11, 2)
        kernel = np.ones((3,3),np.uint8)
        threshold = cv2.dilate(threshold,kernel)

        # trova tutti i contorni
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #estre il contorno dei quadrati
        contours = [c for c in contours if is_square(c)]

        #trova quello della griglia più grande
        biggest_square = contours[0]
        biggest_area = area = cv2.contourArea(biggest_square)

        for contour in contours[1:]:
            area = cv2.contourArea(contour)
            if area > biggest_area:
                biggest_square = contour
                biggest_area = area


        #disegna il contorno trovato
        cv2.drawContours(input_grid_original,biggest_square,-1,[0,0,255],1)

        # calcola la dimensione della griglia
        _,_,w,h = cv2.boundingRect(biggest_square)
        # trova la dimensione della griglia
        cell_dimension = w // 9
        # disegna le griglia più piccole
        for i in range(81):
            # calcola i punti
            row = i // 9
            column = i % 9
            pt1_x = biggest_square[0][0][0] + (column * cell_dimension)
            pt1_y = biggest_square[0][0][1] + (row * cell_dimension)
            pt1 = [pt1_x, pt1_y]
            pt2 = [pt1_x+ cell_dimension, pt1_y + cell_dimension]
            cv2.rectangle(input_grid_original,pt1,pt2, [255,0,0],5)
            print(f'pt1: {pt1}, pt2: {pt2}')


        #mostra l'immagine
        cv2.imshow('sudoku_grid', input_grid_original)

        # attende la pressione di un tasto e poi termina
        cv2.waitKey(0)
    cv2.destroyAllWindows()