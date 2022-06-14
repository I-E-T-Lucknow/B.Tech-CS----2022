#cloth mask
import cv2
import numpy as np
from PIL import Image

# # Reading an image
img = cv2.imread(r'D:\Final Year Project\Attire_Fit_In\datasets\test\cloth\1212.jpg')
img = img.resize(768,1024)
print(img.shape)

# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

# converting the image to HSV format
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print(hsv.shape)

# defining the lower and upper values of HSV,
# this will detect yellow colour
Lower_hsv = np.array([0,0,200], dtype=np.uint8)
Upper_hsv = np.array([0,0,255], dtype=np.uint8)

# creating the mask by eroding,morphing,
# dilating process
Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
Mask = cv2.erode(Mask, kernel, iterations=1)
Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
Mask = cv2.dilate(Mask, kernel, iterations=1)

# Inverting the mask by
# performing bitwise-not operation
Mask = cv2.bitwise_not(Mask)

# Displaying the image
cv2.imshow('Mask', Mask)
cv2.imwrite(r'D:\Final Year Project\Attire_Fit_In\datasets\test\cloth-mask\1212.jpg',Mask)

# waits for user to press any key
# (this is necessary to avoid Python
# kernel form crashing)
cv2.waitKey(0)

# closing all open windows
cv2.destroyAllWindows()

# import cv2
# test_image = cv2.imread(r'D:\Final Year Project\Attire_Fit_In\datasets\test\image-parse\1.png')
# test_image3 = test_image.reshape((-1, 3))[:, :2]
# test_image2 = cv2.imread(r'D:\Final Year Project\Attire_Fit_In\datasets\test\image-parse\00891_00.png')
# test_image4 = test_image2.reshape((-1, 3))[:, :2]

# print(test_image.shape)
# print(test_image3.shape)
# print(test_image2.shape)
# print(test_image4.shape)


from PIL import Image

img = Image.open(r'D:\Final Year Project\Attire_Fit_In\datasets\test\image\2.jpg')
print(img)
img = img.convert('P')
print(img)
# img = img.convert('RGB')
img= img.save(r"D:\Final Year Project\Attire_Fit_In\datasets\test\image\3.jpg")
