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

import toolboxScrabble

FillSize = 90 #Remplissage du plateau
SizeOfPerspective = 500
EdgeProportion = 10

TimeToWait = 1000

im = cv2.imread('plateau.jpg',0)

perspective = CropBoard(im, FillSize, SizeOfPerspective )

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
