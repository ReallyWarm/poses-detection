import math
import cv2
import mediapipe as mp 
import numpy as np
from poseDetect import poseDetect
from classifyPose import getPoseType
from debug import debug

# model_complexity -> 1 for more fps / model_complexity -> 2 for more accuracy
mp_pose = mp.solutions.pose
pose_detection = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Global variables
CAM_RES = 640 # image resolution
MODE = 0 # MODE 0 -> Webcam / MODE 1 -> Image
INFO = range(0) # Range of information for landmarks 

def resize_frame(frame, Resolution:int=640):
    '''
    This function resizes the input frame src on one side to the value of the Resolution.

    It depends on which side is longer. That side will have a value of the Resolution.
    
    Return: 
        frame: resized frame

    '''

    h, w = frame.shape[:2]
    if h < w:
        frame = cv2.resize(frame, (Resolution, int(h/(w/Resolution))))
    else:
        frame = cv2.resize(frame, (int(w/(h/Resolution)), Resolution))

    return frame

def main_image():
    frame = cv2.imread('images/1.jpg')
    frame = resize_frame(frame, Resolution=CAM_RES)
    
    frame, landmarks = poseDetect(frame, pose_detection, info=INFO)

    # If detection found the landmarks
    if landmarks:
        pose_type, pose_angles = getPoseType(landmarks)
        print(pose_type)
    
    while 1:
        cv2.imshow('MediaPipe Image', frame)

        # Exit keys as "z", "q" and "ESCAPE"
        exit_keys = (ord("z"), ord("q"), ord("\x1b"))
        if cv2.waitKey(1) & 0xFF in exit_keys:
            break

def main_webcam():
    cap = cv2.VideoCapture(0)
    current_pose = "None"
    pose_type = "None"
    counters = 0
    
    while 1:
        debugging = []

        success, frame = cap.read()
        if not success:
            print("Empty camera frame.")
            continue
        frame = resize_frame(frame, Resolution=CAM_RES)

        frame, landmarks = poseDetect(frame, pose_detection, info=INFO)

        # If detection found the landmarks
        last_pose = current_pose
        if landmarks:
            current_pose, pose_angles = getPoseType(landmarks)
            debugging = [pose_angles[0],pose_angles[1],pose_angles[2],pose_angles[3]]
        
        # Counting times detection get the same pose type
        if current_pose == last_pose:
            if counters < 15:
                counters += 1
            else:
                pose_type = current_pose
        else:
            counters = 0
            pose_type = "None"

        debugging.append(counters)
        debugging.append(pose_type)

        # Flip the image then show it
        frame = cv2.flip(frame, 1)
        debug(frame, debugging)
        cv2.imshow('MediaPipe Webcam', frame)

        # Exit keys as "z", "q" and "ESCAPE"
        exit_keys = (ord("z"), ord("q"), ord("\x1b"))
        if cv2.waitKey(1) & 0xFF in exit_keys:
            break
    cap.release()
    

if __name__ == '__main__' :
    if MODE == 0:
        main_webcam()
    if MODE == 1:
        main_image()
    cv2.destroyAllWindows()