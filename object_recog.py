import cv2
import numpy as np

# Load webcam capture using VideoCapture, 0 is default webcam
webcam = cv2.VideoCapture(0)

# Empty function
def empty(a):
    pass

def getContours(img, imgContour):
    # Get contours from dilated image
    contours, hier = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    
    # For each contour
    for c in contours:
        # Get area, and if the area of the contour is extremely small, do not draw a contour
        area = cv2.contourArea(c)
        if area > 500:
            # Draw for reference
            cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 2)
            # Calculate the perimeter, and approximates the polygon's curves (Douglas-Pecker alg)
            # Using the approximation, create a minimum bounding rect (no rotation/orientation measure)
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
            # Draw a rectangle using the min bounding rect coords
            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (255, 0, 255), 4)
            # Use rectangle co-ordinates, to calculate the centroid of the rectangle
            avg_x = (x + x + w) // 2
            avg_y = (y + y + h) // 2
            # Draw the centroid point and diagonal line intersection for reference
            imgContour = cv2.line(imgContour, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=1)
            imgContour = cv2.line(imgContour, (x, y+h), (x+w, y), color=(0, 0, 255), thickness=1)
            imgContour = cv2.circle(imgContour, (avg_x, avg_y), radius=3, color=(0, 0, 255), thickness=-1)

            # Return centroid tuple
            return((avg_x, avg_y));


# New CV2 Window named Options, for Threshhold Trackars
cv2.namedWindow("Options")
cv2.resizeWindow("Options", 640, 240)
cv2.createTrackbar("minVal", "Options", 104, 255, empty)
cv2.createTrackbar("maxVal", "Options", 207, 255, empty)

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
    # Dilate the image
    kernel = np.ones((3,3))
    frameDilation = cv2.dilate(frameCanny, kernel, iterations=1)
    
    getContours(frameDilation, frame)

    # Show the canny frame
    cv2.imshow('Preview',frame)

    c = cv2.waitKey(2)
    # Exit on 'ESC'
    if c == 27:
        break

# End frame collecting & kill program
webcam.release()
cv2.destroyAllWindows()