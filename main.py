import sys
import time #sleep function
import numpy as np

from matplotlib import pyplot as plt
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2

import math #to use absolute value function 'fabs'
import pytesseract
from PIL import Image

import ToolboxScrabble as ts

FirstKernelSize = 10 #Remplissage du plateau
SecondKernelSize = 30 #Remplissage du plateau
OutputSize = 500

EdgeProportion = float(90)/float(96)
TimeToSkip= 100
TimeToWait = 0

'''Take picture from camera
im=ts.takePicture()
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ts.ShowImage('coucou',im,0)
'''

im = cv2.imread('PlateauO.jpg',0)
ts.ShowImage('title',im,TimeToSkip)

perspective = ts.CropBoard(im, FirstKernelSize, OutputSize, 0, TimeToSkip)

ts.ShowImage('title',perspective,TimeToWait)

perspective = ts.CropBoard(perspective, SecondKernelSize, OutputSize, 1, TimeToSkip)

ts.ShowImage('Perspective',perspective,TimeToWait)


#get coordinates of all the columns
X_ = ts.getColumnsCoordinates(EdgeProportion,OutputSize)


matrix = ts.getFilledCells(perspective,X_,25,25,105)


print matrix

cv2.line(perspective, (X_[0][0],X_[0][0]), (X_[10][0],X_[0][0]), (0,0,0), 2)

ts.ShowImage('Quadrillage',perspective,TimeToWait)

cell = ts.getNeiborhood(perspective,X_[7][0]+5,X_[7][0]+5,20,20,0)


ts.ShowImage('Cell',cell,0)

letter = ts.getChar(cell )

print letter


'''  
While():
take picture
perspective = RecogniseBoard()
WherePart = TestWherePart(perspective)
TestCases(WherePart)
'''
print("End")
