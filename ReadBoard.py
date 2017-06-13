import sys
import time #sleep function
import numpy as np
import cv2
import math #to use absolute value function 'fabs'
import pytesseract
from PIL import Image

import ToolboxScrabble as ts

#draws the grid that is used to extract the cells from the whole board
def drawGrid(im, positionVector, cellSize):
	for i in range (0,15):
		for j in range (0,15):
			cv2.line(im, (positionVector[i],positionVector[j]), (positionVector[i]+cellSize,positionVector[j]), (0,0,0), 1)
			cv2.line(im, (positionVector[i]+cellSize,positionVector[j]), (positionVector[i]+cellSize,positionVector[j]+cellSize), (0,0,0), 1)
			cv2.line(im, (positionVector[i],positionVector[j]+cellSize), (positionVector[i]+cellSize,positionVector[j]+cellSize), (0,0,0), 1)
			cv2.line(im, (positionVector[i],positionVector[j]), (positionVector[i],positionVector[j]+cellSize), (0,0,0), 1)

def isCellOccupied(img,x,y,cellSize,threshold):

  out = np.empty((cellSize, cellSize))

  for i in range(0,cellSize):
    #ts.ShowImage('Quadrillage',img,10)
    for j in range(0,cellSize):

      out[i][j] = img[x+i][y+j]

  return bool( np.median(out) < threshold)

def getFilledCells(img,positionVector,boardState,cellSize,threshold):

	#create support matrix of 0
	filledmatrix=np.zeros((15, 15), dtype=int)

	#browse the board
	for i in range (0,14):
		for j in range (0,14):
			#check if the cell was already processed
			if(boardState[i][j]==0):
				#check if the cell is occupied or not
				if( isCellOccupied(img,positionVector[i],positionVector[j],cellSize,threshold) ):
					filledmatrix[i][j] = int(1)
				else:
					filledmatrix[i][j] = int(0)

	return filledmatrix

def getChar(im):

	img = np.concatenate((im, im, im, im), axis=1) 

	img = img.astype(np.uint8)
    # Apply dilation and erosion to remove some noise

	#blur = cv2.bilateralFilter(img,9,75,75)

    # Apply threshold to get image with only black and white
  	ret,img = cv2.threshold(img,65,255,cv2.THRESH_BINARY)

  	kernel = np.ones((2,2),np.uint8)
  	erosion = cv2.erode(img,kernel,iterations = 3)

	ts.ShowImage('caca',erosion,0)

	# Write the image after apply opencv to do some ...
	cv2.imwrite("temp_char.png", erosion)

	# Recognize text with tesseract for python
	result = pytesseract.image_to_string(Image.open('temp_char.png'))

	return result[0]

'''
def GetCellCoordinate(x,y,positionVector):
	return (positionVector[x],positionVector[y])
'''

def GetCellImage(img,x,y,cellSize):

  out = np.empty([cellSize, cellSize])
  
  for i in range(0,cellSize):
    for j in range(0,cellSize):
      #print img[x+i][y+j]
      out[i][j] = img[x+i][y+j]

  return out.astype(np.uint8)


def ReadBoard(im, BoardState, positionVector, cellSize):
	for i in range(0,15):
		for j in range(0,15):
			if(BoardState[i][j] == 1):
				getChar(GetCellImage(im, positionVector[i], positionVector[j],cellSize))

