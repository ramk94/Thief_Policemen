import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
import cv2
import time
import imutils




class GestureControl:
    def __init__(self):
        """
        load the model and keep the model during the game
        """
        self.bg=None
        tf.reset_default_graph()
        convnet=input_data(shape=[None,89,100,1],name='input')
        convnet=conv_2d(convnet,32,2,activation='relu')
        convnet=max_pool_2d(convnet,2)
        convnet=conv_2d(convnet,64,2,activation='relu')
        convnet=max_pool_2d(convnet,2)

        convnet=conv_2d(convnet,128,2,activation='relu')
        convnet=max_pool_2d(convnet,2)

        convnet=conv_2d(convnet,256,2,activation='relu')
        convnet=max_pool_2d(convnet,2)

        convnet=conv_2d(convnet,256,2,activation='relu')
        convnet=max_pool_2d(convnet,2)

        convnet=conv_2d(convnet,128,2,activation='relu')
        convnet=max_pool_2d(convnet,2)

        convnet=conv_2d(convnet,64,2,activation='relu')
        convnet=max_pool_2d(convnet,2)

        convnet=fully_connected(convnet,1000,activation='relu')
        convnet=dropout(convnet,0.75)

        convnet=fully_connected(convnet,4,activation='softmax')

        convnet=regression(convnet,optimizer='adam',learning_rate=0.001,loss='categorical_crossentropy',name='regression')

        self.model=tflearn.DNN(convnet,tensorboard_verbose=0)

        # Load Saved Model
        self.model.load("TrainedModel/GestureRecogModel.tfl")


    def get_gesture(self):
        """
        Every time open a window and close it after recognition.
        
        workflow:
        1. open a named window with opencv
        2. recognize the current gesture
        3. close the window
        4. return the predicted categories
        :return:
        """
		# initialize weight for running average
        aWeight = 0.5

        # get the reference to the webcam
        camera = cv2.VideoCapture(0)
	
        # region of interest (ROI) coordinates
        top, right, bottom, left = 10, 350, 225, 590

        # initialize num of frames
        num_frames = 0
        start_recording = False
        count = 0;
        while(True):
		    #get the current frame
            (grabbed,frame) = camera.read()
			
			#Resize the frame
            frame = imutils.resize(frame,width=700)
			
			#flip the frame so that it is not the mirror view
            frame = cv2.flip(frame,1)
			
			#Clone the frame
            clone = frame.copy()
            # get the height and width of the frame
            (height, width) = frame.shape[:2]
            # get the ROI
            roi = frame[top:bottom, right:left]

			
			#Convert the roi to grayscale and blur it
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
				
			# to get the background, keep looking till a threshold is reached
            # so that our running average model gets calibrated
            # draw the segmented hand
            #cv2.imshow("Video Feed", clone)
            if num_frames < 30:
                self.run_avg(gray, aWeight)
                cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

                # display the frame with segmented hand
                cv2.imshow("Video Feed", clone)



            else:
                count = count +1
                # segment the hand region
                hand = self.segment(gray)

                # check whether hand region is segmented
                if hand is not None:
				
                    # if yes, unpack the thresholded image and
                    # segmented region
                    (self.thresholded, segmented) = hand

                    # draw the segmented region and display the frame
                    cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))

                    cv2.imshow("Thesholded", self.thresholded)
                    #start_recording = True

                    cv2.imwrite('Temp.png',self.thresholded)
                    self.resizeImage('Temp.png')
                    
                    if start_recording == True:
                        image = cv2.imread('Temp.png')
                        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        prediction = self.model.predict([gray_image.reshape(89, 100, 1)])
                        result = self.evaluate_gesture(np.argmax(prediction))

                        camera.release()
                        cv2.destroyAllWindows()
                        return result
                

            # increment the number of frames
            num_frames += 1
            
            if(num_frames<20):

                cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

                # display the frame with segmented hand
                cv2.imshow("Video Feed", clone)


                print("calibrating")
            else:
                print("Pose Now") 
            if (count == 60):
                start_recording = True

            
            	
    def resizeImage(self,imageName):
        basewidth = 100
        img = Image.open(imageName)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(imageName)
	
    def run_avg(self,image, aWeight):
    # initialize the background
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(image, self.bg, aWeight)
			
    def evaluate_gesture(self,predicted_class):
        if predicted_class==0:
            return "Palm"
        elif predicted_class==1:
            return "Fist"
        elif predicted_class==2:
            return "Swing"
        elif predicted_class==3:
            return "None"
 
    def segment(self,image, threshold=25):
        # find the absolute difference between background and current frame
        diff = cv2.absdiff(self.bg.astype("uint8"), image)

        # threshold the diff image so that we get the foreground
        thresholded = cv2.threshold(diff,
                                threshold,
                                255,
                                cv2.THRESH_BINARY)[1]

        # get the contours in the thresholded image
        cnts,hiearchy = cv2.findContours(thresholded.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

        # return None, if no contours detected
        if len(cnts) == 0:
            return
        else:
            # based on contour area, get the maximum contour which is the hand
            segmented = max(cnts, key=cv2.contourArea)
            return (thresholded, segmented)

			
#Test the Functionality
#gesture = GestureControl();
#print(gesture.get_gesture())

	

