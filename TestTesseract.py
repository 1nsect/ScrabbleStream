import sys
import cv2
import numpy as np

import math #to use absolute value function 'fabs'
import pytesseract
from PIL import Image

def ShowImage(title,im,time):
	cv2.imshow(title,im)
	cv2.waitKey(time)
	cv2.destroyAllWindows()
	return;



    # Read image with opencv
img = cv2.imread('DecoupeO.jpeg',0)


    # Apply dilation and erosion to remove some noise
kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

cv2.imshow('caca',img)


cv2.imwrite('removed_noise.png', img)

    # Apply threshold to get image with only black and white
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Write the image after apply opencv to do some ...
cv2.imwrite('thres.png', img)


    # Recognize text with tesseract for python
result = pytesseract.image_to_string(Image.open('thres.png'))




print result