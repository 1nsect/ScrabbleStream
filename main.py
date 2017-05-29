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
#from pyimagesearch import imutils

import ToolboxScrabble as ts

#Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - 

FirstKernelSize = 10 #Remplissage du plateau
SecondKernelSize = 10 #Remplissage du plateau
ImageSize = 300 #size of the board's image

EdgeProportion = float(90)/float(96)
TimeToSkip= 0
TimeToWait = 0


#Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - 
'''Take picture from camera
im=ts.takePicture()
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ts.ShowImage('coucou',im,0)
'''

#Create the survey matrix
boardState = np.zeros((15, 15), dtype=int)

# load the query image, compute the ratio of the old height
# to the new height, clone it, and resize it
im = cv2.imread('PlateauO.jpg',0)
ratio = im.shape[0] / 300.0
orig = im.copy()
im = imutils.resize(im, height = ImageSize)

ts.ShowImage('title',im,TimeToSkip)

#first croping
perspective = ts.CropBoard(im, FirstKernelSize, 0, TimeToSkip)

#ts.ShowImage('title',perspective,TimeToWait)

#second croping
perspective = ts.CropBoard(perspective, SecondKernelSize, 1, TimeToSkip)

#ts.ShowImage('Perspective',perspective,TimeToWait)


#get coordinates of all the columns
X_ = ts.getColumnsCoordinates(EdgeProportion,OutputSize)

#Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - 

#Scan the new board state and extract new caramels
newBoardState = ts.getFilledCells(perspective,X_,boardState,25,25,105)

#add the new caramels to the boardState matrix
newBoardState = newBoardState - boardState
boardState = newBoardState

#draw line to know where the columns are
#cv2.line(perspective, (X_[0][0],X_[0][0]), (X_[10][0],X_[0][0]), (0,0,0), 2)
#ts.ShowImage('Quadrillage',perspective,TimeToWait)

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
