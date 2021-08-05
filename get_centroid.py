import cv2
import numpy as np

def getCentroid(img, imgContour):
    # Get contours from dilated image
    contours, hier = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    
    # For each contour
    for c in contours:
        # Get area, and if the area of the contour is extremely small, do not draw a contour
        area = cv2.contourArea(c)
        if area > 1000:
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
            # Point statistics
            text = str(avg_x) + ', ' + str(avg_y)
            imgContour = cv2.putText(imgContour, text,(avg_x+5, avg_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255))

            # Return centroid tuple
            return((avg_x, avg_y));