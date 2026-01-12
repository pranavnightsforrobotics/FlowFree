from pypylon import pylon
import numpy as np
import cv2

# -------------------------------
# Camera setup
# -------------------------------
camera = pylon.InstantCamera(
  pylon.TlFactory.GetInstance().CreateFirstDevice()
)
camera.Open()

camera.PixelFormat.SetValue("BayerGR8")

camera.ExposureAuto.SetValue("Off")
camera.GainAuto.SetValue("Off")

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
num = 1

dist = np.load('./camera/calibration/dist_coeffs.npy')
mtx = np.load('./camera/calibration/old_matrix.npy')

WINDOW = 'thresholds'
cv2.namedWindow(WINDOW)
cv2.createTrackbar("R Low Threshold", WINDOW, 0, 255, lambda x: None)
cv2.createTrackbar("G Low Threshold", WINDOW, 0, 255, lambda x: None)
cv2.createTrackbar("B Low Threshold", WINDOW, 0, 255, lambda x: None)
cv2.createTrackbar("R High Threshold", WINDOW, 255, 255, lambda x: None)
cv2.createTrackbar("G High Threshold", WINDOW, 255, 255, lambda x: None)
cv2.createTrackbar("B High Threshold", WINDOW, 255, 255, lambda x: None)

doProcess = False

while camera.IsGrabbing():
  grab = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
  once = True

  if grab.GrabSucceeded():
    bayer = grab.Array

    RGB = cv2.cvtColor(bayer, cv2.COLOR_BayerGR2RGB)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
      break

    elif key == ord('u'):
      doProcess = True
      once = False

    elif key == ord('s'):
      doProcess = False

    # 2. Show the raw feed
    cv2.imshow(WINDOW, RGB)

    # 3. Live Processing Block
    if doProcess:
      # Undistort
      h, w = RGB.shape[:2]
      newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
      dst = cv2.undistort(RGB, mtx, dist, None, newcameramtx)
      
      x, y, w, h = roi
      dst = dst[y:y+h, x:x+w]

      r_lo = cv2.getTrackbarPos("R Low Threshold", WINDOW)
      g_lo = cv2.getTrackbarPos("G Low Threshold", WINDOW)
      b_lo = cv2.getTrackbarPos("B Low Threshold", WINDOW)
      r_hi = cv2.getTrackbarPos("R High Threshold", WINDOW)
      g_hi = cv2.getTrackbarPos("G High Threshold", WINDOW)
      b_hi = cv2.getTrackbarPos("B High Threshold", WINDOW)

      lower = np.array([r_lo, g_lo, b_lo])
      upper = np.array([r_hi, g_hi, b_hi])
      
      # Create Binary Mask
      mask = cv2.inRange(dst, lower, upper)
      
      # Apply the mask to the 'dst' image
      colored_masked = cv2.bitwise_and(dst, dst, mask=mask)

      cv2.imshow('undistorted frame', dst)
      if not once:
        cv2.imwrite('./camera/homographyFlow.png', dst)
        once = True
      cv2.imshow('binary mask', mask)
      cv2.imshow('colored mask', colored_masked)

  grab.Release()

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# -------------------------------
# Cleanup
# -------------------------------
camera.StopGrabbing()
camera.Close()
cv2.destroyAllWindows()
