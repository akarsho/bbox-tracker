import cv2
import numpy as np

# Load webcam capture using VideoCapture, 0 is default webcam
webcam = cv2.VideoCapture(0)

# Empty function
def empty(a):
    pass

# New CV2 Window named Options, for Threshhold Trackars
cv2.namedWindow("Options")
cv2.resizeWindow("Options", 640, 240)
cv2.createTrackbar("minVal", "Options", 150, 255, empty)
cv2.createTrackbar("maxVal", "Options", 255, 255, empty)

while True:
    # Read input from webcam into frame
    ret, frame = webcam.read() 
    # Resize frame and use frame interpolation
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    
    # Produce a blurred frame
    frameBlur = cv2.GaussianBlur(frame, (7, 7), 1)
    # Produce a grayscale frame
    frameGray = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2GRAY)

    # Get values from trackbar
    minVal = cv2.getTrackbarPos("minVal", "Options")
    maxVal = cv2.getTrackbarPos("maxVal", "Options")

    # Produce an edge-detection fram (Canny algorithm)
    frameCanny = cv2.Canny(frameGray, minVal, maxVal)
    
    # Show the canny frame
    cv2.imshow('Preview',frameCanny)

    c = cv2.waitKey(2)
    # Exit on 'SPACE'
    if c == 32:
        break

# End frame collecting & kill program
webcam.release()
cv2.destroyAllWindows()