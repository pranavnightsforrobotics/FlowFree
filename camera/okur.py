from pypylon import pylon
import cv2

# -------------------------------
# Camera setup
# -------------------------------
camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice()
)
camera.Open()

camera.PixelFormat.SetValue("YCbCr422_8")

camera.ExposureAuto.SetValue("Off")
camera.GainAuto.SetValue("Off")

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# -------------------------------
# OpenCV window + trackbar
# -------------------------------
WINDOW = "Threshold Viewer"
cv2.namedWindow(WINDOW)
cv2.createTrackbar("Threshold", WINDOW, 128, 255, lambda x: None)

# -------------------------------
# Main loop
# -------------------------------
while camera.IsGrabbing():
    grab = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab.GrabSucceeded():
        bayer = grab.Array

        # Convert BayerGR8 → grayscale
        gray = cv2.cvtColor(bayer, cv2.COLOR_RGB2GRAY)

        thresh = cv2.getTrackbarPos("Threshold", WINDOW)

        _, bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

        cv2.imshow(WINDOW, bw)
        cv2.imshow("Normal", bayer)

    grab.Release()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------------------
# Cleanup
# -------------------------------
camera.StopGrabbing()
camera.Close()
cv2.destroyAllWindows()
