import numpy as np

# Source points (Trapezoid corners) - Replace with your actual coordinates
source_pts = [
  [327.0, 178.0],    # 1. Top-Left (Original P_TR)
  [566.0, 188.0],     # 2. Top-Right (Original P_TL)
  [616.0, 294.0],   # 3. Bottom-Right (Original P_BL)
  [221.0, 286.0]     # 4. Bottom-Left (Original P_BR)
]

# Function to calculate Euclidean distance between two points
def distance(pt1, pt2):
  return np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

P_TL, P_TR, P_BR, P_BL = source_pts[0], source_pts[1], source_pts[2], source_pts[3]

# --- Calculate Optimal Width (W) ---
W_top = distance(P_TL, P_TR)
W_bottom = distance(P_BL, P_BR)
W = int(max(W_top, W_bottom))

# --- Calculate Optimal Height (H) ---
H_left = distance(P_TL, P_BL)
H_right = distance(P_TR, P_BR)
H = int(max(H_left, H_right))

print(f"Optimal Output Width (W): {W} pixels")
print(f"Optimal Output Height (H): {H} pixels")