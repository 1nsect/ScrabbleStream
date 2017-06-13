import sys
import time #sleep function
import numpy as np
import cv2
import math #to use absolute value function 'fabs'
import pytesseract
from PIL import Image

import ToolboxScrabble as ts

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

def CropBoard( image, ImageSize, Delay ):
  "Takes the image to find the outer edges, KernelShape=0 -> Ellipse; KernelShape=1 -> Square "
  
  #blur with a square of 9 (recommanded) and a sigma value of 75 (not strong, not too smooth)
  blur = cv2.bilateralFilter(image,9,75,75)
  
  ts.ShowImage('salut', blur, Delay)
  #Threshold binary with 110 as Threshold value. Don't know if the adaptive threshold is better.
  ret,th1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)
  #th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
  ts.ShowImage('salut', th1, Delay)

  '''
  #Create a kernel of size Fillsize to open the thresholded image
  if(KernelShape==0):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(FillSize,FillSize))
  if(KernelShape==1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(FillSize,FillSize))
  #kernel = np.ones((FillSize,FillSize),np.uint8)
  opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
  ts.ShowImage('salut', opening, Delay)
  '''

  #apply Canny Edge algorythm
  canny = cv2.Canny(blur,100,200)
  ts.ShowImage('salut', canny, Delay)
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

  # calculate the perspective transform matrix and warp
  # the perspective to grab the screen
  CorrectionMatrix = cv2.getPerspectiveTransform(rect, dst)
  perspective = cv2.warpPerspective(image, CorrectionMatrix, (ImageSize, ImageSize))
  
  return perspective
