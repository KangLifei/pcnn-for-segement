import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
import cv2
import math
import scipy.misc



def Pcnn(img):
    im = img
    x_len, y_len = im.shape
    F = im
    Y = np.zeros([x_len, y_len], float)
    Q = np.zeros([x_len, y_len], float)
    L = np.zeros([x_len, y_len], float)
    U = np.zeros([x_len, y_len], float)
    beta = 0.4
    fire_num = 0
    n = 0
    M = np.array([[0.7070, 1, 0.7070], [1, 0, 1], [0.7070, 1, 0.7070]])
    i = 0
    j = 0
    Decay = 0.3
    yuzhi = 245
    threshold = np.zeros([x_len, y_len], float)
    # Firate=np.zeros([x_len, y_len])
    V_T = 0.2
    while fire_num <10:
        L = 0.1*sg.convolve2d(Y, M, mode='same')#加了0.1
        U = 0.4 * np.multiply(F, L) + F
        for i in range(0, x_len):
            for j in range(0, y_len):
                # print(i, j)
                # print(U[i,j], threshold[i,j])
                if (U[i, j] > threshold[i, j]):
                    threshold[i, j] = yuzhi
                    Y[i, j] = 1.0
                else:
                    Y[i, j] = 0.0
        threshold = math.exp(-Decay) * threshold + V_T * Y
        fire_num = fire_num + 1

        Y_new = 255 * Y
        # 不加这一步，存储的图片全是黑的
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)#以下四行表示显示图片
        # cv2.imshow('image',Y_new)
        # cv2.waitKey(0)
    return Y_new
img = cv2.imread("C:\\Users\\Administrator\\Desktop\\2.tiff")
r,g,b = cv2.split(img)
def main():
    r1=Pcnn(r)
    g1=Pcnn(g)
    b1=Pcnn(b)
    merged = cv2.merge([r1, g1, b1])

    cv2.imshow('merge', merged)

    cv2.destroyAllWindows()
    cv2.waitKey(0)
main()




    # cv2.imwrite('E:\\test_image\\{}.jpg'.format(str(fire_num)), Y_new)#这一步是自动存储
    #  cv2.namedWindow('image', cv2.WINDOW_NORMAL)#以下四行表示显示图片
    #  cv2.imshow('image',Y_new)
    #  cv2.waitKey(0)
    #  cv2.destroyAllWindows()



















































































































































































































































