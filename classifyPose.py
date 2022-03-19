import math
import mediapipe as mp

mp_pose = mp.solutions.pose

def calculateAngle(landmark1:tuple, landmark2:tuple, landmark3:tuple):
    '''
    This function calculates the angle between three landmarks in 2 dimensions.

    Using the same method as calculating the angle between 2 lines, with landmarks1 and landmarks3 as the ending point of the lines extending from landmark2.
    
    Parameters:
        landmark1 (tuple): the first landmark contained the x, y, and z coordinates. (extending point)
        landmark2 (tuple): the second landmark contained the x, y, and z coordinates. (origin point)
        landmark3 (tuple): the third landmark contained the x, y, and z coordinates. (extending point)
    
    Return:
        angle (float): the angle calculated between three landmarks.
        
    '''

    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # math.atan2 return angle in radians measured from the point and the positive x-axis to the origin (0,0).
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - \
                         math.atan2(y1 - y2, x1 - x2))

    # angle that pass 180 degrees from the positive x-axis will be calculated in negative value from the bottom side of the x-axis.
    if angle < 0:
        # make angle value between 0 and 360 degrees
        angle += 360
    
    return angle

def getPoseType(landmarks:list):
    '''
    This function returns the type of pose and the angles calculated between landmarks.

    Parameters:
        landmarks (list): lists of landmarks from pose detection each contained the x, y, and z coordinates.

    Return:
        pose_type (str): the type of pose.
        pose_angles (list): list of angles calculated between landmarks.
            -> [right_shoulder, left_shoulder, right_elbow, left_elbow]

    '''

    pose_type = "None"

    right_shoulder = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value], 
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], 
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    left_shoulder = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], 
                                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_elbow = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                                 landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])

    left_elbow = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    pose_angles = [right_shoulder, left_shoulder, right_elbow, left_elbow]

    # Lift both shoulders up.
    if 70 < right_shoulder < 110 and 70 < left_shoulder < 110:

        if 55 < right_elbow < 95 and 55 < left_elbow < 95:
            pose_type = "Strong pose"

        if 155 < right_elbow < 185 and 155 < left_elbow < 185:
            pose_type = "T pose"
        
    # Lift right
    elif 70 < right_shoulder < 110:
        if 55 < right_elbow < 95:
            pose_type = "Lifted up right"

    # Lift left
    elif 70 < left_shoulder < 110:
        if 55 < left_elbow < 95:
            pose_type = "Lifted up left"
    
    # Raise both shoulders up.
    if 155 < right_shoulder < 185 and 155 < left_shoulder < 185:
        if 155 < right_elbow < 185 and 155 < left_elbow < 185:
            pose_type = "Raised up"

    # Raise right
    elif 145 < right_shoulder < 185:
        if 135 < right_elbow < 170:
            pose_type = "Raised right"

    # Raise left
    elif 145 < left_shoulder < 185:
        if 135 < left_elbow < 170:
            pose_type = "Raised left"

    # EX
    if 70 < right_shoulder < 145 and 10 < right_elbow < 50 and\
       90 < left_shoulder < 140 and 155 < left_elbow < 185:
        pose_type = "Dab right"

    elif 70 < left_shoulder < 145 and 10 < left_elbow < 50 and\
         90 < right_shoulder < 140 and 155 < right_elbow < 185:
        pose_type = "Dab left"

    return pose_type, pose_angles