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

def CropBoard( image, FillSize, SizeOfReworkedImage, KernelShape ):
  "Takes the image to find the outer edges, KernelShape=0 -> Ellipse; KernelShape=1 -> Square "
  
  #blur with a square of 9 (recommanded) and a sigma value of 75 (not strong, not too smooth)
  blur = cv2.bilateralFilter(image,9,75,75)
  
  ShowImage('salut', blur, 0)
  #Threshold binary with 110 as Threshold value. Don't know if the adaptive threshold is better.
  ret,th1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY)
  #th1 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
  ShowImage('salut', th1, 0)
  #Create a kernel of size Fillsize to open the thresholded image
  if(KernelShape==0):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(FillSize,FillSize))
  if(KernelShape==1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(FillSize,FillSize))
  #kernel = np.ones((FillSize,FillSize),np.uint8)
  opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
  ShowImage('salut', opening, 0)
  #apply Canny Edge algorythm
  canny = cv2.Canny(opening,100,200)

  #Find the outer contour in the opened image and retain only useful points
  contours = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  contour = contours[1][0]
  #print contour
  #calculate the corners with the contour list
  epsilon = 0.1*cv2.arcLength(contour,True)
  approx = cv2.approxPolyDP(contour,epsilon,True)
  
  #print approx
  #Define approx as float32 and define size of the perspectived/croped image
  pts1 = np.float32(approx)
  pts2 = np.float32([[0,0],[SizeOfReworkedImage,0],[SizeOfReworkedImage,SizeOfReworkedImage],[0,SizeOfReworkedImage]])
  
  #Create matrix of perspective transformation
  Correction = cv2.getPerspectiveTransform(pts1,pts2)
  
  #Transform image to get right perspective
  perspective = cv2.warpPerspective(image,Correction,(SizeOfReworkedImage,SizeOfReworkedImage))
  
  

  return perspective


def getCoordinateVector(edgeratio,size):

  coorarray = []

  margin=size-round(size*float(edgeratio))
  sizecell=round((size-margin)/15)

  for i in range(0,15):
   coorarray.append([int(round((margin)/2 + i*sizecell))])
    
  return coorarray

def getFillingMatrix():

 return 0


def getNeiborhood(img,x,y,sizex,sizey,origin):

  out = np.empty((sizex, sizey))
  
  
  for i in range(0,sizex):
    for j in range(0,sizey):
      #print img[x+i][y+j]
      out[i][j] = img[x+i][y+j]
     

  return out.astype(np.uint8)


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


def getFilledCells(board,positionvector,sizecellx,sizecelly,threshold):

  

  fillmatrix=np.zeros((15, 15), dtype=int)
  

  for i in range (0,14):
    
    for j in range (0,14):

      c = getNeiborhood(board,positionvector[i][0],positionvector[j][0],sizecellx,sizecelly,0)
      
      
      if int(c.mean()) > threshold: 
        fillmatrix[i][j] = int(0)

      else:
        fillmatrix[i][j] = int(1)
    


  return fillmatrix 


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


