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
#from pyimagesearch import imutils #can't find that modul...

import ToolboxScrabble as ts

#Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - 

FirstKernelSize = 10 #Remplissage du plateau
SecondKernelSize = 5 #Remplissage du plateau
ImageSize = 300 #size of the board's image
EdgeRatio = float(31)/float(32)
Margin=ImageSize-ImageSize*EdgeRatio
CellSize=int(round((ImageSize-2*Margin)/19.38))

#get coordinates of all the columns
X_ = ts.getColumnsCoordinates(Margin,CellSize)

TimeToSkip= 100
TimeToWait = 2000


#Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - 
'''Take picture from camera
im=ts.takePicture()
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ts.ShowImage('coucou',im,0)
'''

#Create the survey matrix
boardState = np.zeros((15, 15), dtype=int)

# load the query image
# to the new height, clone it, and resize it
im = cv2.imread('PlateauO.jpg')
orig = im.copy()
im = cv2.resize(im,None,ImageSize,0.5,0.5, interpolation = cv2.INTER_AREA)

# convert the image to grayscale
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ts.ShowImage('title',gray,TimeToSkip)

#first croping
perspective = ts.CropBoard(gray, FirstKernelSize, 0, TimeToSkip)

#ts.ShowImage('title',perspective,TimeToWait)

#second croping
perspective = ts.CropBoard(perspective, SecondKernelSize, 1, TimeToSkip)

ts.ShowImage('Perspective',perspective,TimeToSkip)

#Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - 

#Scan the new board state and extract new caramels
newFilledCells = ts.getFilledCells(perspective,X_,boardState,CellSize,210)

print newFilledCells

#add the new filled cells to the boardState matrix
boardState = boardState + newFilledCells

#draw line to know where the columns are
#cv2.line(perspective, (X_[0][0],X_[0][0]), (X_[10][0],X_[0][0]), (0,0,0), 2)
ts.ShowImage('Quadrillage',perspective,TimeToWait)



#ts.ShowImage('Cell',cell,TimeToWait)

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
