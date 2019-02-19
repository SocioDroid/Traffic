import cv2
import numpy as np
import sys
import os

filename = sys.argv[1]
noplate = sys.argv[2]+'.jpg'
print("INSIDE VIDEO")
print(filename)
print(noplate)
flag = False
cap = cv2.VideoCapture(filename)
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        cv2.imwrite(noplate, frame)
        flag = True
    if flag:
        break

os.system("python uploadFTP.py "+noplate)
cap.release()
cv2.destroyAllWindows()

