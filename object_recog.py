import cv2

#Load webcam capture using VideoCapture, 0 is default webcam
webcam = cv2.VideoCapture(0)


while True:
    #Read input from webcam into frame
    ret, frame = webcam.read() 
    #Resize frame and use frame interpolation
    frame = cv2.resize(frame, None, fx=1.25, fy=1.25, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('Preview',frame)
    c = cv2.waitKey(2)
    #Exit on 'ESC'
    if c == 32:
        break

#End frame collecting & kill program
webcam.release()
cv2.destroyAllWindows()