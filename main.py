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

import ToolboxScrabble as ts

KernelSize = 10 #Remplissage du plateau
OutputSize = 500
EdgeProportion = 10

TimeToWait = 1000

im = cv2.imread('plateau.jpg',0)

perspective = ts.CropBoard(im, KernelSize, OutputSize )

ts.ShowImage('title',perspective,0)

perspective = ts.CropBoard(perspective, KernelSize, OutputSize)

ts.ShowImage('Perspective',perspective,0)



SizeCell = (OutputSize-2*OutputSize/EdgeProportion)/15

pt1 =  (OutputSize/EdgeProportion + 6*SizeCell, OutputSize/EdgeProportion + SizeCell)
pt2 =  (OutputSize/EdgeProportion  + 6*SizeCell, 9*OutputSize/EdgeProportion - SizeCell)

cv2.line(perspective, pt1, pt2, (0,0,0), 2)

ts.ShowImage('Quadrillage',perspective,0)

'''
While():
take picture
perspective = RecogniseBoard()
WherePart = TestWherePart(perspective)
TestCases(WherePart)
'''
print("End")
