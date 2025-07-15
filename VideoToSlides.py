# import OpenCV
import cv2
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

print(totalFrames)
# reset to the first frame
video.set(cv2.CAP_PROP_POS_FRAMES, 0)
check, firstFrame = video.read()

video.set(cv2.CAP_PROP_POS_FRAMES, totalFrames)
check, lastFrame = video.read()

cv2.imwrite('firstFrame.png', firstFrame)

cv2.imwrite('lastFrame.png', lastFrame)