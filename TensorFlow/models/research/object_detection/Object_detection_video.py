# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

def count_frames_manual(video):
	# initialize the total number of frames read
	total = 0
 
	# loop over the frames of the video
	while True:
		# grab the current frame
		(grabbed, frame) = video.read()
	 
		# check to see if we have reached the end of the
		# video
		if not grabbed:
			break
 
		# increment the total number of frames read
		total += 1
 
	# return the total number of frames in the video file
	return total

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
VIDEO_NAME = sys.argv[1]

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Path to video
PATH_TO_VIDEO = os.path.join(CWD_PATH,VIDEO_NAME)

# Number of classes the object detector can identify
NUM_CLASSES = 2

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Open video file
video = cv2.VideoCapture(PATH_TO_VIDEO)
video2 = cv2.VideoCapture(PATH_TO_VIDEO)
filename="testoutput.avi"
codec=cv2.VideoWriter_fourcc('m','p','4','v')#fourcc stands for four character code
framerate=10
resolution=(1920,1080)
VideoFileOutput=cv2.VideoWriter(filename,codec,framerate, resolution)
VideoFileOutput2=cv2.VideoWriter("testoutput2.avi",codec,framerate, resolution)
count = 0
threshold = 0.9
itration = 0
while(video.isOpened()):
    objects = []
    i=0
    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    ret, frame = video.read()
    frame_expanded = np.expand_dims(frame, axis=0)
    width = 1920#int(video.get(3))  # float
    height = 1080#int(video.get(4)) # float
    # Perform the actual detection by running the model with the image as input
    try:
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})
       
        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=2,
            min_score_thresh=0.80)
    except TypeError:
       break
    if not objects :
        #cv2.imwrite("test_images/frame%d.jpg" % count, frame)
        VideoFileOutput2.write(frame)
        
        count = count + 1
        objects1 = []
        for index, value in enumerate(classes[0]):
            object_dict = {}
            if scores[0, index] > threshold:
                object_dict[(category_index.get(value)).get('name').encode('utf8')] = scores[0, index]
                objects1.append(object_dict)
        
        try:
            if b'nohelmet' in objects1[0].keys():
    	        #print("NoHelmet Found")
                
                ymin = int((boxes[0][0][0]*height))
                xmin = int((boxes[0][0][1]*width))
                ymax = int((boxes[0][0][2]*height))
                xmax = int((boxes[0][0][3]*width))
        
                Result = np.array(frame[ymin:ymax,xmin:xmax])
                cv2.imwrite('cropped/tested_video_cropped'+str(itration)+'.jpg',Result)
                itration = itration + 1
                print(itration)
        except IndexError:
    	    pass
    VideoFileOutput.write(frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break
print("Object detection")
# Clean up
os.system("python openALPR.py testoutput2.avi")
video.release()
cv2.destroyAllWindows()
