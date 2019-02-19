import sys
import os
import cv2
import re
os.system("pwd")
file_name=sys.argv[1]
noplat = ""
threeshold = 0
with open(file_name) as f:
    for line in f:
        if 'confidence:' in line:
            pos = line.find(':')
            posend = line.find('\n')
            confi = float(line[pos+2:posend])

            if confi > threeshold:
                noplat = line
                threeshold = confi

dash = noplat.find('-')
dash = dash +2
noplat = noplat[dash:]
blank = noplat.find(" ")
noplat = noplat[:blank]


noplat=re.sub("[^a-zA-Z0-9]+", "", noplat) 
print(noplat)

v_file = str(sys.argv[2])

os.system('python video.py '+v_file+' '+noplat) 

#+v_file+' '+noplat)

# imageName=noplat+'.jpg'
# #CAPTURE IMAGE OF THE RIDER
# v_file = str(sys.argv[2])
# cap = cv2.VideoCapture(v_file)
# flag = False
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret == True:
#         cv2.imwrite(imageName, frame)
#         flag = True
#     if flag:
#         break
