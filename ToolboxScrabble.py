import sys
import time #sleep function
import cv2
import numpy as np
import math #to use absolute value function 'fabs'
import pytesseract

def ShowImage(title,im,time):
  cv2.imshow(title,im)
  cv2.waitKey(time)
  cv2.destroyAllWindows()
  return;

def CropBoard( image, FillSize, SizeOfReworkedImage ):
  "Takes the image to find the outer edges"
  
  #blur with a square of 9 (recommanded) and a sigma value of 75 (not strong, not too smooth)
  blur = cv2.bilateralFilter(image,9,75,75)
  
  #Threshold binary with 110 as Threshold value. Don't know if the adaptive threshold is better.
  ret,th1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)
  #th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
  
  #Create a kernel of size Fillsize to open the thresholded image 
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(FillSize,FillSize))
  #kernel = np.ones((FillSize,FillSize),np.uint8)
  opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
  
  #apply Canny Edge algorythm
  canny = cv2.Canny(opening,100,200)

  #Find the outer contour in the opened image and retain only useful points
  contour = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  contour = contour[0][0]

  #calculate the corners with the contour list
  epsilon = 0.1*cv2.arcLength(contour,True)
  approx = cv2.approxPolyDP(contour,epsilon,True)
  
  #Define approx as float32 and define size of the perspectived/croped image
  pts1 = np.float32(approx)
  pts2 = np.float32([[0,0],[SizeOfReworkedImage,0],[SizeOfReworkedImage,SizeOfReworkedImage],[0,SizeOfReworkedImage]])
  
  #Create matrix of perspective transformation
  Correction = cv2.getPerspectiveTransform(pts1,pts2)
  
  #Transform image to get right perspective
  perspective = cv2.warpPerspective(image,Correction,(SizeOfReworkedImage,SizeOfReworkedImage))
  
  

  return perspective


