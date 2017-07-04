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
import PictureAcquisition as pa
import ReadBoard as rb

#Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - Setting - 

ImageSize = 1000 #size of the board's image
EdgeRatio = float(31)/float(32)
Margin=ImageSize-ImageSize*EdgeRatio
CellSize=int(round((ImageSize-2*Margin)/15))

#Il faudra calibrer cette valeur
Threshold = 110

#get coordinates of all the columns
X_ = ts.getColumnsPixelPosition(Margin,CellSize)

print X_

TimeToSkip= 100
TimeToWait = 4000


#Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - Init - 
'''Take picture from camera
im=pa.takePicture()
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ts.ShowImage('coucou',im,0)
'''

#Create the survey matrix
boardState = np.zeros((15, 15), dtype=object)

# load the query image
# to the new height, clone it, and resize it
im = cv2.imread('PlateauO.jpg')
orig = im.copy()
im = cv2.resize(im,None,ImageSize,0.5,0.5, interpolation = cv2.INTER_AREA)

# convert the image to grayscale
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ts.ShowImage('title',gray,TimeToSkip)

#croping
perspective = pa.CropBoard(gray, ImageSize, TimeToSkip)

ts.ShowImage('Perspective',perspective,TimeToSkip)

#Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - Loop - 

#Scan the new board state and extract new caramels
newFilledCells = rb.getFilledCells(perspective,X_,boardState,CellSize,Threshold)

print newFilledCells

#add the new filled cells to the boardState matrix
boardState = boardState + newFilledCells

#draw line to know where the columns are


rb.drawGrid(perspective.copy(), X_, CellSize)

rb.ReadBoard(perspective,boardState,X_,CellSize)

print boardState


#letter = rb.getChar(perspective, 7, 7, CellSize)
#print letter


'''  
While():
Protocole de calibration
'''

print("End")
