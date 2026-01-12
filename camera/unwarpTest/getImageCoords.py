import cv2
import numpy as np

def getPixelLoc(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONDOWN:
    print(f"Coordinates (x, y): ({x}, {y})")

img = cv2.imread('./camera/postBrighten.png')

window_name = 'Image with Pixel Location Tool'

cv2.imshow(window_name, img)
cv2.setMouseCallback(window_name, getPixelLoc, img)

cv2.waitKey(0)
cv2.destroyAllWindows()