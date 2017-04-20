import sys
import cv2
import numpy as np
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


print("Hello World")


im = cv2.imread('plateau.jpg',0)

cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

ret,th1 = cv2.threshold(im,230,255,cv2.THRESH_BINARY)

cv2.imshow('image',th1)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernel = np.ones((20,20),np.uint8)
opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)


cv2.imshow('image',opening)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(opening.max())

mask=np.corrcoef(opening,opening)



cv2.imshow('image',mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

out=np.zeros(opening.shape)