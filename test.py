import sys
import time #sleep function
import cv2
import numpy as np
from matplotlib import pyplot as plt
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math #to use absolute value function 'fabs'

TailleRemplissage = 90 #Remplissage du plateau
tolerance = 20
SizeOfPerspective = 500
EdgeProportion = 10

TimeToWait = 1000

print("Hello World")

im = cv2.imread('plateau.jpg',0)

cv2.imshow('Plateau',im)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

blur = cv2.bilateralFilter(im,9,75,75)

cv2.imshow('Blur',blur)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

ret,th1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)

cv2.imshow('Threshold',th1)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

kernel = np.ones((TailleRemplissage,TailleRemplissage),np.uint8)
opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)

cv2.imshow('Remplissage',opening)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(opening, contours, -1, (100,0,100), 1)

cv2.imshow('Contours',opening)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

contour = contours[1] #ne plus avoir le cadre de l'image

epsilon = 0.1*cv2.arcLength(contour,True)
approx = cv2.approxPolyDP(contour,epsilon,True)

cv2.drawContours(opening, approx, -1, (255,255,255), 4)

cv2.imshow('Opening',opening)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

pts1 = np.float32(approx)
pts2 = np.float32([[0,0],[SizeOfPerspective,0],[SizeOfPerspective,SizeOfPerspective],[0,SizeOfPerspective]])

Correction = cv2.getPerspectiveTransform(pts1,pts2)

perspective = cv2.warpPerspective(im,Correction,(SizeOfPerspective,SizeOfPerspective))

cv2.imshow('Perspective',perspective)
cv2.waitKey(TimeToWait)
cv2.destroyAllWindows()

pt1 =  (SizeOfPerspective/EdgeProportion, SizeOfPerspective/EdgeProportion)
pt2 =  (SizeOfPerspective/EdgeProportion, 9*SizeOfPerspective/EdgeProportion)

(SizeOfPerspective-2*SizeOfPerspective/EdgeProportion)/15

cv2.line(perspective, pt1, pt2, (0,0,0), 2)

cv2.imshow('Quadrillage',perspective)
cv2.waitKey(1000)
cv2.destroyAllWindows()

print("End")