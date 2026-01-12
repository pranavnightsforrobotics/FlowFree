import numpy as np
import cv2

# --- 1. Define Points ---

# Source points (Trapezoid corners in the original image)
# Make sure they are ordered: top-left, top-right, bottom-right, bottom-left
source_pts = [
  [327.0, 178.0],    # 1. Top-Left (Original P_TR)
  [566.0, 188.0],     # 2. Top-Right (Original P_TL)
  [616.0, 294.0],   # 3. Bottom-Right (Original P_BL)
  [221.0, 286.0]     # 4. Bottom-Left (Original P_BR)
]

# Define the dimensions of the desired output rectangle (W x H)
W = 395  # Example Width
H = 151  # Example Height

# Destination points (Rectangle corners)
dest_pts = [
  [0, 0],      # Top-Left
  [W - 1, 0],  # Top-Right
  [W - 1, H - 1],  # Bottom-Right
  [0, H - 1]   # Bottom-Left
]

# --- 2. Calculate the Homography Matrix ---

# M is the 3x3 transformation matrix
M = cv2.getPerspectiveTransform(np.float32(source_pts), np.float32(dest_pts))

# Load the original image
original_image = cv2.imread('./camera/homographyFlow.png') 

# --- 3. Apply the Transformation ---

# warped_image will be the final rectangle
warped_image = cv2.warpPerspective(
  original_image,  # The input image
  M,               # The transformation matrix
  (W, H),          # The size of the output image (Width, Height)
  flags=cv2.INTER_LINEAR
)

# Display or save the result
# cv2.imwrite('corrected_rectangle.jpg', warped_image)
cv2.imshow('Warped Image', warped_image)
cv2.imshow('Initial Image', original_image)
cv2.imwrite('./camera/postHomographFlow.png', warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()