import os
import sys
video_name = sys.argv[1]
os.system('alpr -c in '+video_name+' >> out.txt')
os.system('python get_plate_no.py out.txt '+video_name)
get_plate_no.py
