# import OpenCV
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import time
import os

def SaveVideoFrames(curVideo, folderNum):
    # load the video that we want to use
    video = cv2.VideoCapture(curVideo)

    # get the number of frames in the video
    totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    start = time.time()
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
    # Pre testing before going through whole video
    for frame in range(5,totalFrames,5):
    # reset to the first frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame)
        check, curFrame = video.read()
        # convert image to gray scale
        # SSIM works best with grayscale and reduces channels from 3 to 1
        # instead of seeing the amount of RGB in each pixel, we just see brightness
        # more efficient
        curGray = cv2.cvtColor(curFrame, cv2.COLOR_BGR2GRAY)

        video.set(cv2.CAP_PROP_POS_FRAMES, frame-5)
        check, prevFrame = video.read()
        prevGray = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)

        # SSIM requires both input images to be same height and width
        # sometimes the frames might be different in size because of video encoding, 
        # cropping during recording, or reading from different sources
        min_h = min(curGray.shape[0], prevGray.shape[0])
        min_w = min(curGray.shape[1], prevGray.shape[1])

        # crop the frames to the right width
        curGray = curGray[:min_h, :min_w]
        prevGray = prevGray[:min_h, :min_w]
        score = ssim(curGray, prevGray)
        if score < 0.99:
            cv2.imwrite(f'Video{folderNum}/firstFrame{frame}.png', curFrame)
            # print("different slide")
    end = time.time()
    print(f"Elapsed time: {end}-{start}")
    # cv2.imwrite('lastFrame.png', lastFrame)

videoArray = ["output_fixed.mp4", "Video2.mov"]
for i,vid in enumerate(videoArray):
    os.makedirs(f"Video{i}", exist_ok=True)
    SaveVideoFrames(vid, i)