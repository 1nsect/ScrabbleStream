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

def CropBoard( image, FillSize, KernelShape, showImageTime ):
  "Takes the image to find the outer edges, KernelShape=0 -> Ellipse; KernelShape=1 -> Square "
  
  #blur with a square of 9 (recommanded) and a sigma value of 75 (not strong, not too smooth)
  blur = cv2.bilateralFilter(image,9,75,75)
  
  ShowImage('salut', blur, showImageTime)
  #Threshold binary with 110 as Threshold value. Don't know if the adaptive threshold is better.
  ret,th1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)
  #th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
  ShowImage('salut', th1, showImageTime)
  #Create a kernel of size Fillsize to open the thresholded image
  if(KernelShape==0):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(FillSize,FillSize))
  if(KernelShape==1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(FillSize,FillSize))
  #kernel = np.ones((FillSize,FillSize),np.uint8)
  opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
  ShowImage('salut', opening, showImageTime)

  #apply Canny Edge algorythm
  canny = cv2.Canny(opening,100,200)

  #Find the outer contour in the opened image and retain only useful points - we copy the image because findcontours
  #is destructive
  (contours, _) = cv2.findContours(canny.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

  #sort the contours so that we have the largest contour
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
  
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

  # now that we have our rectangle of points, let's compute
  # the width of our new image
  (tl, tr, br, bl) = rect
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

  # ...and now for the height of our new image
  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
   
  # take the maximum of the width and height values to reach
  # our final dimensions
  maxWidth = max(int(widthA), int(widthB))
  maxHeight = max(int(heightA), int(heightB))

  # construct our destination points which will be used to
  # map the screen to a top-down, "birds eye" view
  dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
 
  # calculate the perspective transform matrix and warp
  # the perspective to grab the screen
  CorrectionMatrix = cv2.getPerspectiveTransform(rect, dst)
  perspective = cv2.warpPerspective(image, CorrectionMatrix, (maxWidth, maxHeight))
  
  return perspective

#get X coordinates of all the column
def getColumnsCoordinates(edgeratio,size):

  coorarray = []

  margin=size-round(size*float(edgeratio))
  sizecell=round((size-margin)/15)

  for i in range(0,15):
   coorarray.append([int(round((margin)/2 + i*sizecell))])
    
  return coorarray

def getFillingMatrix():

 return 0


def isCellOccupied(img,x,y,sizex,sizey,threshold):

  out = np.empty((sizex, sizey))
  
  
  for i in range(0,sizex):
    for j in range(0,sizey):
      #print img[x+i][y+j]
      out[i][j] = img[x+i][y+j]
  
  return int( out.mean() > threshold)

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


def getFilledCells(board,positionVector,boardState,sizecellx,sizecelly,threshold):

  #create support matrix of 0
  filledmatrix=np.zeros((15, 15), dtype=int)
  
  #browse the board
  for i in range (0,14):
    for j in range (0,14):
      #check if the cell was already processed
      if(boardState[i][j]==0):
      #check if the cell is occupied or not
        if( isCellOccupied(board,positionVector[i][0],positionVector[j][0],sizecellx,sizecelly,threshold) ):
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


