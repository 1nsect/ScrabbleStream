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
EdgeProportion = 37

TimeToSkip= 100
TimeToWait = 3000

im = cv2.imread('plateau.jpg',0)

perspective = ts.CropBoard(im, KernelSize, OutputSize )

ts.ShowImage('title',perspective,TimeToSkip)

perspective = ts.CropBoard(perspective, KernelSize, OutputSize)

ts.ShowImage('Perspective',perspective,TimeToSkip)



SizeCell = (OutputSize-2*OutputSize/EdgeProportion)/15

pt1 =  (OutputSize/EdgeProportion, OutputSize/EdgeProportion)
pt2 =  (OutputSize/EdgeProportion, OutputSize/EdgeProportion + 15*SizeCell)

cv2.line(perspective, pt1, pt2, (0,0,0), 2)

ts.ShowImage('Quadrillage',perspective,TimeToWait)

'''
While():
take picture
perspective = RecogniseBoard()
WherePart = TestWherePart(perspective)
TestCases(WherePart)
'''
print("End")
