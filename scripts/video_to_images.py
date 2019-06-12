import numpy as np
import cv2
import uuid

cap = cv2.VideoCapture('output.avi')
count = 0
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame is None:
        break
    if count % 50 == 0:
        cv2.imwrite('../data/pics/output/{}.jpg'.format(uuid.uuid1()), frame)
    count += 1
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
