# -*- coding: utf-8 -*-
import cv2


def to_roi(image):

    first_point = (0, 0)
    second_aux_point = (0, 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, otsu_threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret, binary_threshold = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    # Punto de arriba a la izquierda del área de trabajo
    for i in xrange(image.shape[1]-1, 0, -1):
        if otsu_threshold[0, i] != 0:
            first_point = (i, 0)
            break
    # # Punto de abajo a la izquierda del área de trabajo (auxiliar, hay que disminuirlo)
    for i in xrange(image.shape[0]-1, 0, -1):
        if binary_threshold[i, first_point[0]] != 0:
            second_aux_point = (first_point[0], i)
            break
    first_aux_middle_point = (0, 0)
    for i in xrange(second_aux_point[1], 0, -1):
        if binary_threshold[i, 2*binary_threshold.shape[1]/4] != 0:
            first_aux_middle_point = (2*binary_threshold.shape[1]/4, i)
            break
    # cv2.circle(image, first_aux_middle_point, 1, (0, 0, 255), 3)
    second_aux_middle_point = (0, 0)
    for i in xrange(second_aux_point[1], 0, -1):
        if binary_threshold[i, 3*binary_threshold.shape[1]/4] != 0:
            second_aux_middle_point = (3*binary_threshold.shape[1]/4, i)
            break
    # cv2.circle(image, second_aux_middle_point, 1, (0, 0, 255), 3)
    # Punto de abajo a la izquierda definitivo
    second_point = (second_aux_point[0], first_aux_middle_point[1] + (first_aux_middle_point[1] - second_aux_middle_point[1]))
    # cv2.circle(img, second_point, 1, (0, 0, 255), 3)
    # Punto de abajo a la derecha
    third_point = (binary_threshold.shape[1], second_aux_middle_point[1] + (second_aux_middle_point[1] - first_aux_middle_point[1]))
    # cv2.circle(img, third_point, 1, (0, 0, 255), 3)

    first_roi_point = first_point

    if second_point[1] > third_point[1]:
        # cv2.line(img, (second_aux_point[0], second_point[1]), (img.shape[1], second_point[1]), (0, 255, 0), 2)
        # cv2.line(img, first_point, (second_aux_point[0], second_point[1]), (0, 255, 0), 2)
        second_roi_point = (image.shape[1], second_point[1])

    else:
        # cv2.line(img, (second_aux_point[0], third_point[1]), (img.shape[1], third_point[1]), (0, 255, 0), 2)
        # cv2.line(img, first_point, (second_aux_point[0], third_point[1]), (0, 255, 0), 2)
        second_roi_point = (image.shape[1], third_point[1])

    return image[first_roi_point[1]:second_roi_point[1], first_point[0]:second_roi_point[0]]

if __name__ == '__main__':
    name = 'at4'
    img = cv2.imread(name + '.tif')
    window_title = 'img'
    roi_img = to_roi(img)
    cv2.imshow(window_title, roi_img)
    cv2.waitKey(0) & 0xFF
