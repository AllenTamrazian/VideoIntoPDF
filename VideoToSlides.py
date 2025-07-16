# import OpenCV
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

videoArray = ["Video1.mov", "Video2.mov"]

# load the video that we want to use
video = cv2.VideoCapture(videoArray[0])

# get the number of frames in the video
totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# video.set(cv2.CAP_PROP_POS_FRAMES, totalFrames-1) gives an error
# so find the last working frame
while True:
    # set the video frame to the last one
    video.set(cv2.CAP_PROP_POS_FRAMES, totalFrames)
    # check if it is working and get the current frame
    check, curFrame = video.read()
    # if it is not working or the current frame is null, 
    if not check or curFrame is None or curFrame.size == 0:
        # decrease the index of the current frame
        totalFrames -= 1
        continue
    # if we are successful, break the loop
    break

# Pre testing before going through whole video

# reset to the first frame
video.set(cv2.CAP_PROP_POS_FRAMES, 0)
check, firstFrame = video.read()
# convert image to gray scale
# SSIM works best with grayscale and reduces channels from 3 to 1
# instead of seeing the amount of RGB in each pixel, we just see brightness
# more efficient
first_gray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)

video.set(cv2.CAP_PROP_POS_FRAMES, 1)
check, lastFrame = video.read()
last_gray = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)

# SSIM requires both input images to be same height and width
# sometimes the frames might be different in size because of video encoding, 
# cropping during recording, or reading from different sources
min_h = min(first_gray.shape[0], last_gray.shape[0])
min_w = min(first_gray.shape[1], last_gray.shape[1])

# crop the frames to the right width
first_gray = first_gray[:min_h, :min_w]
last_gray = last_gray[:min_h, :min_w]
score = ssim(first_gray, last_gray)
print(score)
# cv2.imwrite('firstFrame.png', firstFrame)

# cv2.imwrite('lastFrame.png', lastFrame)