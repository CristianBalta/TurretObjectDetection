from threading import Thread
import serial
import cv2
import numpy as np
import time

from VideoStream import VideoStream
from Parameters import Parameters
from Model import Model


class InitialiseVideoStream():
    t = None

    def __init__(self):
        self.videostream = None
        self.lista = []

    #def start(self):
        # Start the thread that reads frames from the video stream
        #Thread(target=self.compute(), args=()).start()
        #return self


    def stream(self):

        parameters = Parameters()
        model = Model(parameters.PATH_TO_CKPT)

        # Initialize frame rate calculation
        frame_rate_calc = 1
        freq = cv2.getTickFrequency()

        # Initialize video stream
        self.videostream = VideoStream(resolution=(parameters.imW, parameters.imH), framerate=30)

        self.videostream.start()

        time.sleep(1)

        # for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        while True:

            # Start timer (for calculating frame rate)
            t1 = cv2.getTickCount()

            # Grab frame from video stream
            frame1 = self.videostream.read()

            # Acquire frame and resize to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (model.width, model.height))
            input_data = np.expand_dims(frame_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if model.floating_model:
                input_data = (np.float32(input_data) - model.input_mean) / model.input_std

            # Perform the actual detection by running the model with the image as input
            model.interpreter.set_tensor(model.input_details[0]['index'], input_data)
            model.interpreter.invoke()

            # Retrieve detection results
            boxes = model.interpreter.get_tensor(model.output_details[0]['index'])[
                0]  # Bounding box coordinates of detected objects
            classes = model.interpreter.get_tensor(model.output_details[1]['index'])[
                0]  # Class index of detected objects
            scores = model.interpreter.get_tensor(model.output_details[2]['index'])[0]  # Confidence of detected objects
            # num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > parameters.min_conf_threshold) and (scores[i] <= 1.0)):
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1, (boxes[i][0] * parameters.imH)))
                    xmin = int(max(1, (boxes[i][1] * parameters.imW)))
                    ymax = int(min(parameters.imH, (boxes[i][2] * parameters.imH)))
                    xmax = int(min(parameters.imW, (boxes[i][3] * parameters.imW)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                    if self.lista.__len__() < 2:
                        self.lista.append((xmin+ xmax)/2)


                    # with serial.Serial('COM4', 9600) as ser:
                    #     print(ser.read())
                    #     ser.close()

                    # Draw label
                    object_name = parameters.labels[
                        int(classes[i])]  # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                                  (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),
                                  cv2.FILLED)  # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                                2)  # Draw label text

            # Draw framerate in corner of frame
            cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 0), 2,
                        cv2.LINE_AA)

            # All the results have been drawn on the frame, so it's time to display it.
            cv2.imshow('Press q to quit.', frame)

            # Calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2 - t1) / freq
            frame_rate_calc = 1 / time1



            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break

        # Clean up
        cv2.destroyAllWindows()
        self.videostream.stop()
        print(self.lista)





