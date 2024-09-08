
#TEST FEATURE. STILL NOT COMPLETE

#program used to auto generate new training data from a foundation model


    #this program needs to take in a video file and project name
    #also needs to take in the foundation model
    #files will be saved to project name/autodata /images and /labels

#foundation model for testing = './Model1/train/weights/last.pt'
#training video for testing = video_3.mp3
#project name for testing is Test

def auto_annotate(project_name, training_video, foundation_model):

    import cv2
    from ultralytics import YOLO

    #parameters
    THRESHOLD = 0.5 #confidence level for an object to be detected

    #open the video
    video = cv2.VideoCapture(training_video)

    try:
        model = YOLO(foundation_model)
    except Exception as e:
        print('Model Not Found')
        video.release
        cv2.destroyAllWindows()
        exit()

    #variable used to track number of detections in new video and increment file names
    detect_count = 0

    #play frame by frame
    while video.isOpened():
        ret, frame = video.read() #ret is a true/false if a frame was returned. frame is frame

        if not ret:
            print('Error Reading Frame. Frame end.')
            break

        #array of all detects in the current frame
        results = model.predict(frame, conf=THRESHOLD)

        annotation_data =  '0 '


        #coordinates from that result converted to .txt string format
        coordinates = (results[0].boxes.xywhn.tolist())
        for coordinate in coordinates:
            for i in range(4):
                annotation_data += f'{str((round(coordinate[i], 6)))} '
        

        #if an object was detected then write annotation and frame to files
        if len(results[0].boxes) > 0:
        #need a special folder to save them in
        #need to save the frame
            cv2.imwrite(f'./{project_name}/autodata/images/{detect_count}.jpg', frame)
        #need to save coordinates as text
            f = open(f'./{project_name}/autodata/labels/{detect_count}.txt', 'w')
            f.write(annotation_data)
            f.close()
            detect_count += 1
        

    video.release()
    cv2.destroyAllWindows()


def main():
    model = './Model1/train/weights/last.pt'
    video = 'video_3.mp4'
    project = 'Model1'

    auto_annotate(project,video,model)

main()
