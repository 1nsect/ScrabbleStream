import sys
import time #sleep function
import cv2
import numpy as np
from matplotlib import pyplot as plt
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math #to use absolute value function 'fabs'
import pytesseract

#import toolbox.py

TailleRemplissage = 90 #Remplissage du plateau
SizeOfPerspective = 500
EdgeProportion = 10

TimeToWait = 1000



def ShowImage(title,im,time):
	cv2.imshow(title,im)
	cv2.waitKey(time)
	cv2.destroyAllWindows()
	return;
'''
def sort4Corner(listin):

	for i in range(0,3)
		for j in range(0,3)
	
			if listin[i][j] 

	return(listout);

'''


im = cv2.imread('plateau.jpg',0)

blur = cv2.bilateralFilter(im,9,75,75)

th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
ShowImage('opening',th1 ,0)

kernel = np.ones((TailleRemplissage,TailleRemplissage),np.uint8)
opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)

ShowImage('opening',opening,0)

canny = cv2.Canny(opening,100,200)

ShowImage('canny',canny,0)



contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


cv2.drawContours(canny, contours, -1, (100,0,100), 1)

ShowImage('contour',canny,0)


contour = contours[1] #ne plus avoir le cadre de l'image

epsilon = 0.1*cv2.arcLength(contour,True)
approx = cv2.approxPolyDP(contour,epsilon,True)

cv2.drawContours(opening, approx, -1, (255,255,255), 4)


'''
approx=sort4Corner(approx)
'''
pts1 = np.float32(approx)
pts2 = np.float32([[0,0],[SizeOfPerspective,0],[SizeOfPerspective,SizeOfPerspective],[0,SizeOfPerspective]])

Correction = cv2.getPerspectiveTransform(pts1,pts2)

perspective = cv2.warpPerspective(im,Correction,(SizeOfPerspective,SizeOfPerspective))

ShowImage('Perspective',perspective,0)



SizeCell = (SizeOfPerspective-2*SizeOfPerspective/EdgeProportion)/15

pt1 =  (SizeOfPerspective/EdgeProportion + 6*SizeCell, SizeOfPerspective/EdgeProportion + SizeCell)
pt2 =  (SizeOfPerspective/EdgeProportion  + 6*SizeCell, 9*SizeOfPerspective/EdgeProportion - SizeCell)

cv2.line(perspective, pt1, pt2, (0,0,0), 2)

ShowImage('Quadrillage',perspective,0)





'''
While():
take picture
perspective = RecogniseBoard()
WherePart = TestWherePart(perspective)
TestCases(WherePart)
'''
print("End")