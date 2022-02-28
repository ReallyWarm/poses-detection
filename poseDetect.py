import cv2
import mediapipe as mp 
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def poseDetect(frame, pose_detection, info=range(0)):
    '''
    This function uses the pose detection solution from Mediapipe to find the landmarks and draw on the input image.

    Parameters:
        frame: the input image
        pose_detection (Pose): mediapipe.solutions.pose.Pose solution
        info (range): range for the optional information about landmarks
    
    Return:
        output_frame: the image with drawn landmarks
        landmarks (list): lists of landmarks from pose detection each contained the x, y, and z coordinates.

        (optional) info: informations of landmarks are print in the terminal.

    '''

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    output_frame = frame.copy()
    output_frame.flags.writeable = False

    # Prepare frame in RGB format for pose landmark detection
    rgb_frame = cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB)
    pose = pose_detection.process(rgb_frame)

    landmarks = []
    if pose.pose_landmarks:
        # Draw pose landmarks on the output image
        mp_drawing.draw_landmarks(output_frame, pose.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        # Append all landmarks position into the list of (x, y, z)
        h, w = output_frame.shape[:2]
        for lm in pose.pose_landmarks.landmark:
            landmarks.append((int(lm.x * w), int(lm.y * h), int(lm.z * w)))

        # Print landmarks information in range
        if info is not range(0):
            for i in info:
                # Normalized landmarks.
                print(f'{mp_pose.PoseLandmark(i).name}:')
                print(f'{pose.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value]}')
                
                # Landmarks after converting them into their original scale.
                h, w = frame.shape[:2]
                print(f'Scaled Position:')
                print(f'x: {pose.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x * w}')
                print(f'y: {pose.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y * h}')
                print(f'z: {pose.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].z * w}')
                # print(f'visibility: {pose.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].visibility}\n')

    return output_frame, landmarks
