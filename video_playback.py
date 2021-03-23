# importing libraries 
import cv2 
import numpy as np 
import argparse

# import arguments
parser = argparse.ArgumentParser(description='Video Player')
parser.add_argument('--video_file_path', dest='video_file_path', type=str, help='File path of the video')
parser.add_argument('--fps', dest='fps', type=str, help='Framerate')
parser.add_argument('--display_resolution_width', dest='display_resolution_width', type=int, help='Width resolution')
parser.add_argument('--display_resolution_height', dest='display_resolution_height', type=int, help='Height resolution')
parser.add_argument('--monochrome', dest='monochrome', type=bool, help='Monochrome filter')
args = parser.parse_args()



# press p to pause b to step back a frame

video_file_path = args.video_file_path
fps = args.fps 
display_resolution_width = args.display_resolution_width
display_resolution_height= args.display_resolution_height
monochrome = args.monochrome
# Use default if arguments have not been provided
if args.video_file_path is None:
    video_file_path = 'video_1.mp4'
    fps = 30
    monochrome = False
    display_resolution_width = 1280
    display_resolution_height = 720
# Create a VideoCapture object and read from input file 
cap = cv2.VideoCapture(video_file_path)
cap.set(cv2.CAP_PROP_FPS, fps) # set frame rate 

# retrieve the total number of frames
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
def change_res(display_resolution_width,display_resolution_height):
    cap.set(3, display_resolution_width)
    cap.set(4, display_resolution_height)
change_res(display_resolution_width,display_resolution_height)

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# Check if camera opened successfully 
if (cap.isOpened()== False):  
  print("Error opening video  file") 
   
# Read until video is completed 
while(cap.isOpened()): 
      
  # Capture frame-by-frame 
  ret, frame = cap.read()
  frame150 = rescale_frame(frame, percent=400)
  grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  (thresh, blackAndWhiteFrame) = cv2.threshold(grayFrame, 127, 255, cv2.THRESH_BINARY) 
  if ret == True:
    # make video monochrome 
    if monochrome == True:
      cv2.imshow('video bw', blackAndWhiteFrame)
    else:
    # Display the resulting frame 
      cv2.imshow('Frame', frame150) 
    key = cv2.waitKey(1) & 0xff
    if key == ord('p'):
      # sleep here until a valid key is pressed
        while (True):
            key = cv2.waitKey(0)

            # check if 'p' is pressed and resume playing
            if (key & 0xFF == ord('p')):
                break

            # check if 'b' is pressed and rewind video to the previous frame. You must press p to resume playing again.
            if (key & 0xFF == ord('b')):
                cur_frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
                print('* At frame #' + str(cur_frame_number))

                prev_frame = cur_frame_number
                if (cur_frame_number > 1):
                    prev_frame -= 1

                print('* Rewind to frame #' + str(prev_frame))
                cap.set(cv2.CAP_PROP_POS_FRAMES, prev_frame)

    # Press Q on keyboard to  exit 
    if cv2.waitKey(25) & 0xFF == ord('q'): 
      break
   
  # Break the loop 
  else:  
    break
   
# When everything done, release  
# the video capture object 
cap.release() 
   
# Closes all the frames 
cv2.destroyAllWindows() 

