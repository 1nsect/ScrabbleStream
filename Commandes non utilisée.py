#Commandes non utilisée

#threshold adapté au contour du pixel:

th2 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,10)

cv2.imshow('image',th2)
cv2.waitKey(0)
cv2.destroyAllWindows()

th3 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,10)

cv2.imshow('image',th3)
cv2.waitKey(0)
cv2.destroyAllWindows()


'''
'''

#trouver centroid
MCentroid = cv2.moments(contour)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

#angel de rotation
angle = math.atan(float(approx[1][0][1]- approx[0][0][1])/float(approx[1][0][0]- approx[0][0][0]))

#Matrice de rotation
MRotation = cv2.getRotationMatrix2D((cx,cy),angle,1)
rotation = cv2.warpAffine(im,MRotation,im.shape)

M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
