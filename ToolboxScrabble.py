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

#get X coordinates of all the columns
def getColumnsCoordinates(margin,cellSize):

  coorarray = []

  for i in range(0,15):
   coorarray.append([int(round((margin)/2 + i*cellSize))])
    
  return coorarray





