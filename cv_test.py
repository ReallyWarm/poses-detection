import cv2, time, argparse
import numpy as np
from fps import FPS

if __name__ == '__main__' :
    cap = cv2.VideoCapture(0)
    fps = FPS()

    while 1:
        run, frame = cap.read()
        if not run:
            break

        # cv2.rectangle(frame, (30, 30), (60, 60), (0, 255, 0), 3)

        fps.update()
        fps.draw(frame)
        cv2.imshow("CAM", frame)

        if cv2.waitKey(1) == ord("z"):
            break

    cap.release()
    cv2.destroyAllWindows()