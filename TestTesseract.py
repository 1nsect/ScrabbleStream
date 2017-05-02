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


img_path = 'DecoupeO2.jpg'



img = cv2.imread(img_path)
img = np.concatenate((img, img, img, img), axis=1)

    # Convert to gray
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise

blur = cv2.bilateralFilter(img,9,75,75)

    # Apply threshold to get image with only black and white
ret,img = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)

kernel = np.ones((2,2),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 4)

ShowImage('caca',erosion,1000)

    # Write the image after apply opencv to do some ...
cv2.imwrite("thres.png", erosion)

    # Recognize text with tesseract for python
result = pytesseract.image_to_string(Image.open('thres.png'))

print result