
#the video_parse function now works as expected
#some improvements can still be made
#takes in 3 values
    #file - should be a .mp4 video file... NOT SURE IF I CAN USE OTHERS?
    #path - should be set durring config task of set up but should results in "./photos/frame_name.jpg"
    #rate - if rate is 1 it will save 1 photo for every 1 second of video

import cv2 
import numpy

def video_parse(video_file, save_path, rate):

    #need to save video into folder location as well

    #need to validate path is correct?
    #need to ensure frame rate is a realistic time interval. 

    #open video file
    video = cv2.VideoCapture(video_file)

    #set initial frame count
    frame_name = 0
    frame_count = 0 

    #loop thorugh video frames and save to file path using rate calculation
    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            print('fail')
            break

        if frame_count % rate == 0:
            filename = str(frame_name)
            save_file = (save_path + "/" + filename + ".jpg") #name of the file

            resized_frame = cv2.resize(frame, (400,300))

            cv2.imwrite(save_file, resized_frame)
            frame_name+=1
   
                
        else:
            frame_count+=1

    video.release()
    cv2.destroyAllWindows()