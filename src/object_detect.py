
#program used to validate a model by viewing result over a live video

#this function will take in a video and a model and play the results live for a viewer to see

#video_path = 'video_3.mp4'
#model_path = './Model1/train/weights/last.pt'

def object_detect(video_path, model_path):

    import cv2
    from ultralytics import YOLO

    #parameters
    THRESHOLD = 0.5 #confidence level for an object to be detected

    #open the video
    video = cv2.VideoCapture(video_path)

    try:
        model = YOLO(model_path)
    except Exception as e:
        print('Model Not Found')
        video.release
        cv2.destroyAllWindows()
        exit()


    #play frame by frame
    while video.isOpened():
        ret, frame = video.read() #ret is a true/false if a frame was returned. frame is frame

        if not ret:
            print('Error Reading Frame. Frame end.')
            break

        results = model.predict(frame, conf=THRESHOLD)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        cv2.imshow('frame' , annotated_frame)
        if cv2.waitKey(1) == ord('q'):
            break


    video.release()
    cv2.destroyAllWindows()


def main():
    video_path = 'video_3.mp4'
    model_path = './Model1/train/weights/last.pt'

    object_detect(video_path, model_path)

main()