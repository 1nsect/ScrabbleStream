import sys
import time #sleep function
import numpy as np
import cv2
import math #to use absolute value function 'fabs'
import pytesseract
from PIL import Image



def ShowImage(title,im,time):
  cv2.imshow(title,im)
  cv2.waitKey(time)
  cv2.destroyAllWindows()
  return;

def CropBoard( image, ImageSize, showImageTime ):
  "Takes the image to find the outer edges, KernelShape=0 -> Ellipse; KernelShape=1 -> Square "
  
  #blur with a square of 9 (recommanded) and a sigma value of 75 (not strong, not too smooth)
  blur = cv2.bilateralFilter(image,9,75,75)
  
  ShowImage('salut', blur, showImageTime)
  #Threshold binary with 110 as Threshold value. Don't know if the adaptive threshold is better.
  ret,th1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)
  #th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
  ShowImage('salut', th1, showImageTime)

  '''
  #Create a kernel of size Fillsize to open the thresholded image
  if(KernelShape==0):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(FillSize,FillSize))
  if(KernelShape==1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(FillSize,FillSize))
  #kernel = np.ones((FillSize,FillSize),np.uint8)
  opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
  ShowImage('salut', opening, showImageTime)
  '''

  #apply Canny Edge algorythm
  canny = cv2.Canny(blur,100,200)
  ShowImage('salut', canny, showImageTime)
  #Find the outer contour in the opened image and retain only useful points - we copy the image because findcontours
  #is destructive
  (contours, _) = cv2.findContours(canny.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

  #sort the contours so that we have the 10 largest contours
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
  
  #reverse order to have the 10 largest contour but in the smallest to largest order
  contours.reverse()

  #initialize the board contour
  contour = None

  # loop over our contours
  for c in contours:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
      contour = approx
      break

  # now that we have our screen contour, we need to determine
  # the top-left, top-right, bottom-right, and bottom-left
  # points so that we can later warp the image -- we'll start
  # by reshaping our contour to be our finals and initializing
  # our output rectangle in top-left, top-right, bottom-right,
  # and bottom-left order
  pts = contour.reshape(4, 2)
  rect = np.zeros((4, 2), dtype = "float32")

  # the top-left point has the smallest sum whereas the bottom-right has the largest sum
  s = pts.sum(axis = 1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]
  
  # compute the difference between the points -- the top-right
  # will have the minumum difference and the bottom-left will
  # have the maximum difference
  diff = np.diff(pts, axis = 1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]

  # construct our destination points which will be used
  dst = np.array([[0, 0],[ImageSize - 1, 0],[ImageSize - 1, ImageSize - 1],[0, ImageSize - 1]], dtype = "float32")
  print dst

  # calculate the perspective transform matrix and warp
  # the perspective to grab the screen
  CorrectionMatrix = cv2.getPerspectiveTransform(rect, dst)
  perspective = cv2.warpPerspective(image, CorrectionMatrix, (ImageSize, ImageSize))
  
  return perspective

#get X coordinates of all the columns
def getColumnsCoordinates(margin,cellSize):

  coorarray = []

  for i in range(0,15):
   coorarray.append([int(round((margin)/2 + i*cellSize))])
    
  return coorarray

#draws the grid that is used to extract the cells from the whole board
def drawGrid(im, positionVector, cellSize):
  for i in range (0,15):
    for j in range (0,15):
      cv2.line(im, (positionVector[i][0],positionVector[j][0]), (positionVector[i][0]+cellSize,positionVector[j][0]), (0,0,0), 1)
      cv2.line(im, (positionVector[i][0]+cellSize,positionVector[j][0]), (positionVector[i][0]+cellSize,positionVector[j][0]+cellSize), (0,0,0), 1)
      cv2.line(im, (positionVector[i][0],positionVector[j][0]+cellSize), (positionVector[i][0]+cellSize,positionVector[j][0]+cellSize), (0,0,0), 1)
      cv2.line(im, (positionVector[i][0],positionVector[j][0]), (positionVector[i][0],positionVector[j][0]+cellSize), (0,0,0), 1)

def isCellOccupied(img,x,y,cellSize,threshold):

  out = np.empty((cellSize, cellSize))

  for i in range(0,cellSize):
    #ShowImage('Quadrillage',img,10)
    for j in range(0,cellSize):

      out[i][j] = img[x+i][y+j]

  return bool( np.median(out) < threshold)

def getChar(im):

  img = np.concatenate((im, im, im, im), axis=1) 

  img = img.astype(np.uint8)
    # Apply dilation and erosion to remove some noise

  #blur = cv2.bilateralFilter(img,9,75,75)

    # Apply threshold to get image with only black and white
  ret,img = cv2.threshold(img,65,255,cv2.THRESH_BINARY)

  kernel = np.ones((2,2),np.uint8)
  erosion = cv2.erode(img,kernel,iterations = 3)

  ShowImage('caca',erosion,0)

  # Write the image after apply opencv to do some ...
  cv2.imwrite("temp_char.png", erosion)

  # Recognize text with tesseract for python
  result = pytesseract.image_to_string(Image.open('temp_char.png'))

  return result[0]


def getFilledCells(img,positionVector,boardState,cellSize,threshold):

  #create support matrix of 0
  filledmatrix=np.zeros((15, 15), dtype=int)

  #browse the board
  for i in range (0,14):
    for j in range (0,14):
      #check if the cell was already processed
      if(boardState[i][j]==0):
      #check if the cell is occupied or not
        if( isCellOccupied(img,positionVector[i][0],positionVector[j][0],cellSize,threshold) ):
          filledmatrix[i][j] = int(1)
        else:
          filledmatrix[i][j] = int(0)
  
  return filledmatrix


def takePicture():
  camera_port = 1

#Number of frames to throw away while the camera adjusts to light levels
  ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
  camera = cv2.VideoCapture(camera_port)

# Captures a single image from the camera and returns it in PIL format

 # read is the easiest way to get a full image out of a VideoCapture object.
  retval, im = camera.read()
  
  return im  


