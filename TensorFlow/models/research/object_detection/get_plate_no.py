import sys
import os
import cv2

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
print(noplat)
noplat.strip()

#CAPTURE IMAGE OF THE RIDER

video_name = sys.argv[2]

video = cv2.VideoCapture(video_name)

count = 0
while(video.isOpened()):
    ret, frame = video.read()
    count = count +1
    cv2.imwrite('detected_images/'+noplat+str(count)+'.jpg', frame)
    if ret == False :
        break


video.release()
