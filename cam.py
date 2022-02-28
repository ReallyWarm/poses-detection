import math
import cv2
import mediapipe as mp 
import numpy as np
from debug import debug

mp_face_detection = mp.solutions.face_detection
mp_pose = mp.solutions.pose

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

CAM_RES = 640

def resize_frame(frame):
    h, w = frame.shape[:2]
    if h < w:
        frame = cv2.resize(frame, (CAM_RES, int(h/(w/CAM_RES))))
    else:
        frame = cv2.resize(frame, (int(w/(h/CAM_RES)), CAM_RES))

    return frame

def main():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) as face_detection, \
         mp_pose.Pose(model_complexity=1, min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose_detection:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Empty camera frame.")
                continue
            frame = resize_frame(frame)

            # To improve performance, optionally mark the image as not writeable to pass by reference.
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face = face_detection.process(frame)
            pose = pose_detection.process(frame)

            # Draw the face detection annotations on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if face.detections:
                for detection in face.detections:
                    mp_drawing.draw_detection(frame, detection)

            mp_drawing.draw_landmarks(frame, pose.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            # Flip the image horizontally for a selfie-view display.
            frame = cv2.flip(frame, 1)
            debug(frame, [(frame.shape[1],frame.shape[0]), pose.pose_landmarks])
            cv2.imshow('MediaPipe Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord("z"):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__' :
    main()